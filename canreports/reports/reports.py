from django.db import transaction, connection


class SQLReport(object):
    sql = ""  # Overwrite this in the subclasses

    def execute(self):
        with connection.cursor() as cursor:
            cursor.execute(self.sql)
            row = self.dictfetchall(cursor)

        return row

    @staticmethod
    def dictfetchall(cursor):
        # Return all rows from a cursor as a dict
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class PucsMessageReport(SQLReport):
    # Calculates some stats about can/gps messages.
    # This should only return 1 row.
    #
    # {
    #     "total_can": 1099032.0,
    #     "total_gps": 63843.0,
    #     "total_runtime": 74098.0,
    #     "unique_can_count": 61,
    #     "avg_can_per_sec": 17.208405098174303,
    #     "avg_gps_per_sec": 0.9996398709798641,
    #     "timestamp_with_least_cans": "2016-10-28T08:56:35",
    #     "timestamp_with_most_cans": "2016-10-28T11:51:28"
    # }

    # The "pucs_messages_per_timestamp" view isn't materialized, so it'll execute every time.
    # And we need it's results for both "stats" and "min_max", so we'll bring it in as a temp
    # table and calculate the stats/min_max here (vs separate views), so it only gets executed once.
    sql = """CREATE TEMP TABLE tmp_timestamped AS SELECT * FROM pucs_messages_per_timestamp;"""

    # Calculate the stats of the puc messages...
    sql += """
    CREATE TEMP TABLE stats AS
        SELECT
            SUM(num_of_can) AS total_can,
            SUM(num_of_gps) AS total_gps,
            AVG(num_of_can) AS avg_can_per_sec,
            AVG(num_of_gps) AS avg_gps_per_sec,
            MIN(timestamp) AS start_timestamp,
            MAX(timestamp) AS end_timestamp
        FROM tmp_timestamped;
    """

    # For each timestamp with x # of can messages, take the earliest.
    # Then, for the smallest and largest counts, grab the timestamps for our min/max values
    sql += """
    CREATE TEMP TABLE min_maxes AS
    WITH temp1 AS (
        SELECT DISTINCT ON (num_of_can) num_of_can, timestamp
            FROM tmp_timestamped
            ORDER BY num_of_can ASC, timestamp ASC
    ) SELECT * FROM (
        SELECT timestamp AS min_timestamp
        FROM temp1
        LIMIT 1
    ) t1, (
        SELECT timestamp AS max_timestamp
        FROM temp1
        ORDER BY num_of_can DESC
        LIMIT 1
    ) t2;
    """

    # The longer SELECT makes sure it's an index-only scan on "header", much faster than the rows.
    sql += """
    CREATE TEMP TABLE unique_cans AS
    SELECT COUNT(*) as unique_can_count FROM (SELECT DISTINCT header FROM pucs_canmessage) t;
    """

    # This is our main statement, using results of the temp tables we made
    sql += """
    SELECT
        total_can,
        total_gps,
        extract(epoch from end_timestamp - start_timestamp) AS total_runtime,  -- In seconds
        unique_can_count,
        avg_can_per_sec,
        avg_gps_per_sec,
        min_maxes.min_timestamp AS timestamp_with_least_cans,
        min_maxes.max_timestamp AS timestamp_with_most_cans
    FROM stats, unique_cans, min_maxes;
    """
