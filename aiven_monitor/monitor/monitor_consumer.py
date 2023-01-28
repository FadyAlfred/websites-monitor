import json
import os
from logging import getLogger, Logger
from typing import Dict, Optional

import psycopg
from kafka import KafkaConsumer

from aiven_monitor.dto import MonitorRecord
from aiven_monitor.repo import MonitorRecordRepo, WebsiteRepo


class MonitorConsumer:
    def __init__(
            self, kafka_consumer: KafkaConsumer, website_repo: WebsiteRepo,
            monitor_record_repo: MonitorRecordRepo, logger: Logger, keep_consumer_alive: Optional[bool] = True):
        self.kafka_consumer = kafka_consumer
        self.website_repo = website_repo
        self.monitor_record_repo = monitor_record_repo
        self.logger = logger
        self.keep_consumer_alive = keep_consumer_alive

    def handle_monitor(self, message_value: Dict):
        monitor_record = MonitorRecord(
            site_id=message_value.get('site_id'),
            response_time=message_value.get('response_time'),
            status_code=message_value.get('status_code'),
            is_content_matched=message_value.get('is_content_matched'),
        )
        # TODO validate that record added and make a retry police in case not
        self.monitor_record_repo.add(monitor_record)

    def run_consumer(self):
        while True:
            for message in self.kafka_consumer.poll().values():
                self.logger.info('Message received with the following value %s', message[0].value.decode('utf-8'))
                self.handle_monitor(json.loads(message[0].value.decode('utf-8')))

            if not self.keep_consumer_alive:
                break

    @classmethod
    def create(cls):
        db_connection = psycopg.connect(
            user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), dbname=os.getenv('DB_NAME')
        )
        website_repo = WebsiteRepo.create(db_connection)
        monitor_record_repo = MonitorRecordRepo.create(db_connection)

        return cls(
            KafkaConsumer(
                os.getenv('KAFKA_TOPIC'),
                bootstrap_servers=f'{os.getenv("KAFKA_HOST")}:{os.getenv("KAFKA_PORT")}',
                security_protocol='SSL',
                ssl_cafile=os.getenv('KAFKA_SSL_CAFILE_PATH'),
                ssl_certfile=os.getenv('KAFKA_SSL_CERTFILE_PATH'),
                ssl_keyfile=os.getenv('KAFKA_SSL_KEYFILE_PATH'),
            ),
            website_repo,
            monitor_record_repo,
            getLogger(__name__)
        )
