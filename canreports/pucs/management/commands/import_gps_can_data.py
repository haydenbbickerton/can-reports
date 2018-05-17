# -*- coding: utf-8 -*-
#
# This imports the gps_can_data.csv I was given into the database.
#
# Note: It takes like 5 min, in production (and if it was frequently used) I'd probably
# add support for cursor.executemany rather than Model.objects.bulk_create. TODO
#
from django.core.management.base import BaseCommand, CommandError
from canreports.pucs.models import Puc, CanMessage, GpsMessage
import os
import logging
import pandas as pd
import numpy as np

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import gps_can_data.csv into database.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', nargs=1, type=str)

    def handle(self, *args, **options):
        csv_path = options['csv_path'][0]
        if not os.path.exists (csv_path):
            raise CommandError ("{} doesnt exist.".format(csv_path))

        df = pd.read_csv(csv_path, sep=',', dtype=object)  # dtype as object to preserve original data

        # REMOVE AFTER DEBUGGING
        # df = df.head(5000)

        print('Loading CAN/GPS data into the database, this will take a minute....')
        # Get unique PUCs, insert them
        pucs = [Puc(id=x) for x in df['puc_id'].unique()]

        Puc.objects.bulk_create(pucs)
        print("PUCs inserted")
        logger.info("PUCs inserted")

        # # No timezone was included with data, I'll go with UTC since Django wants it
        # df['ts'] = pd.to_datetime(df['ts'], utc=True)

        # Insert CAN Messages
        can_messages = (
            df[~df['message_id'].isnull()]
            [['message_id', 'dlc', 'payload', 'puc_id', 'ts']]
            .rename(index=str, columns={'message_id': 'header', 'ts': 'timestamp'})
            .to_dict('records')
        )

        can_inserted = 0
        for batch in chunks(can_messages, 10000):
            can_batch = [CanMessage(**x) for x in batch]
            CanMessage.objects.bulk_create(can_batch)
            can_inserted += 10000
            print("Can Messages Inserted: {}".format(can_inserted))

        logger.info("CAN Messages inserted")

        # Insert GPS Messages
        gps_messages = (
            df[df['message_id'].isnull()]
            [['latitude', 'longitude', 'groundspeed', 'truecourse', 'puc_id', 'ts']]  # gps_id
            .rename(index=str, columns={
                # 'gps_id': 'id',
                'ts': 'timestamp'})
            .to_dict('records')
        )

        gps_inserted = 0
        for batch in chunks(gps_messages, 10000):
            gps_batch = [GpsMessage(**x) for x in batch]
            GpsMessage.objects.bulk_create(gps_batch)
            gps_inserted += 10000
            print("GPS Messages Inserted: {}".format(gps_inserted))

        print("GPS Messages inserted")
        logger.info("GPS Messages inserted")
