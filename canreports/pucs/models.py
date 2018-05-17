import uuid
import simplejson as json
from django.db import connection
from django.db import models
from django.forms.models import model_to_dict
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_pgviews import view as pg

from canreports import redis


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # auto ints for internal, uuid for external
    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True


class Puc(BaseModel):
    # Passive Uplink Connection
    #
    # Normally I'd reserve the autoint PK for internal use, and have a "number"
    # field for the external ID. But I'm guessing that "puc_id" comes from the
    # DB id, so I'll do it here to match.
    id = models.PositiveIntegerField(primary_key=True)


class CanMessage(BaseModel):
    # If this wasn't a demo, I'd probably pull the PGN from the header and have
    # a FK to a table full of data from the J1939 companion spreadsheet.
    # In an ETL, I'd decode the payload to make reports easier
    header = models.CharField(max_length=8, db_index=True)  # Used to specify the data type of a CAN message payload.
    dlc = models.SmallIntegerField("Data Length Code")
    payload = models.CharField(max_length=16)
    timestamp = models.DateTimeField()
    puc = models.ForeignKey(
        Puc,
        on_delete=models.CASCADE,
        related_name="can_messages",
        related_query_name="can_message"
    )

    class Meta(BaseModel.Meta):
        get_latest_by = "timestamp"
        ordering = ('timestamp',)


class GpsMessage(BaseModel):
    # number = models.IntegerField(primary_key=True)  # In the data sample, every gps_id was unique.
    latitude = models.DecimalField(decimal_places=14, max_digits=17)
    longitude = models.DecimalField(decimal_places=14, max_digits=17)
    groundspeed = models.DecimalField(decimal_places=14, max_digits=17)
    truecourse = models.DecimalField(decimal_places=14, max_digits=17)
    timestamp = models.DateTimeField()
    puc = models.ForeignKey(
        Puc,
        on_delete=models.CASCADE,
        related_name="gps_messages",
        related_query_name="gps_message",
    )

    class Meta(BaseModel.Meta):
        get_latest_by = "timestamp"
        ordering = ('timestamp',)

    def as_json(self):
        return {
            'id': self.id,
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'groundspeed': str(self.groundspeed),
            'truecourse': str(self.truecourse),
            'timestamp': self.timestamp .strftime('%Y-%m-%d %H:%M:%S'),
            'puc_id': self.puc_id
        }


@receiver(post_save, sender=GpsMessage, dispatch_uid="publish_gps_message_info")
def publish_gps_message_info(sender, instance, **kwargs):
    redis.publish('canreports', json.dumps(instance.as_json()))

# =============================================================================
#
#   DB Views
#
#   https://www.postgresql.org/docs/9.2/static/sql-createview.html
#
# =============================================================================

class PucMessagesPerTimestamp(pg.ReadOnlyView):
    # Counts can/gps messages, grouping by timestamp
    #
    #        timestamp          num_of_can   num_of_gps
    # ------------------------ ------------ ------------
    #  2016-10-28 05:00:00+00           10            1
    #  2016-10-28 05:00:01+00           10            1

    class Meta:
      app_label = 'pucs'
      db_table = 'pucs_messages_per_timestamp'
      managed = False

    sql = """
    SELECT timestamp, SUM(can) AS num_of_can, SUM(gps) as num_of_gps
    FROM (
      SELECT timestamp, 1 can, 0 gps FROM pucs_canmessage
      UNION ALL
      SELECT timestamp, 0 can, 1 gps FROM pucs_gpsmessage
    ) z
    GROUP BY timestamp
    ORDER BY timestamp ASC
    """
