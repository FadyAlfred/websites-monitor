import asyncio
import json
import os
import re
import time
from logging import getLogger, Logger
from typing import List, Optional

import aiohttp
import psycopg
from kafka import KafkaProducer

from aiven_monitor.dto import MatchedContentEnum, MonitorRecord, Website
from aiven_monitor.repo import WebsiteRepo


class MonitorProducer:
    def __init__(self, kafka_producer: KafkaProducer, website_repo: WebsiteRepo, logger: Logger) -> None:
        self.kafka_producer = kafka_producer
        self.website_repo = website_repo
        self.logger = logger

    @staticmethod
    def _match_payload(payload: str, regex: Optional[str]) -> MatchedContentEnum:
        if regex:
            if re.search(regex, payload):
                is_content_matched = MatchedContentEnum.MATCHED
            else:
                is_content_matched = MatchedContentEnum.UNMATCHED
        else:
            is_content_matched = MatchedContentEnum.NO_REGEX

        return is_content_matched

    async def _run_health_check(self, websites: List[Website]) -> None:
        async with aiohttp.ClientSession() as session:
            for website in websites:
                self.logger.info('Run health check on %s', website.url)
                start = time.perf_counter()
                async with session.get(website.url, ssl=False) as response:
                    response_time = time.perf_counter() - start
                    response_body = await response.text()
                    is_content_matched = self._match_payload(response_body, website.regex)
                    monitor_record = MonitorRecord(
                        site_id=website.id,
                        status_code=str(response.status),
                        response_time=response_time,
                        is_content_matched=is_content_matched
                    )
                    monitor_record_dict = monitor_record.as_dict()
                    self.logger.info(
                        'Send monitor record about website %s with following record %s',
                        website.url, monitor_record_dict
                    )
                    self.kafka_producer.send(
                        os.getenv('KAFKA_TOPIC'), json.dumps(monitor_record_dict).encode('utf-8')
                    )

    def run_producer(self) -> None:
        websites = self.website_repo.fetch_all()
        asyncio.run(self._run_health_check(websites))

        self.kafka_producer.close()
        self.website_repo.db_connection.close()

    @classmethod
    def create(cls):
        db_connection = psycopg.connect(
            user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), dbname=os.getenv('DB_NAME')
        )
        website_repo = WebsiteRepo.create(db_connection)

        return cls(
            KafkaProducer(
                bootstrap_servers=f'{os.getenv("KAFKA_HOST")}:{os.getenv("KAFKA_PORT")}',
                security_protocol='SSL',
                ssl_cafile=os.getenv('KAFKA_SSL_CAFILE_PATH'),
                ssl_certfile=os.getenv('KAFKA_SSL_CERTFILE_PATH'),
                ssl_keyfile=os.getenv('KAFKA_SSL_KEYFILE_PATH'),
            ),
            website_repo,
            getLogger(__name__)
        )
