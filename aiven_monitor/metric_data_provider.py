import os
from logging import getLogger, Logger
from typing import List

import psycopg

from aiven_monitor.dto import MetricItem
from aiven_monitor.repo import MonitorRecordRepo


# TODO all get get metric methods here should support offset and limit
class MetricDataProvider:
    def __init__(self, monitor_record_repo: MonitorRecordRepo, logger: Logger):
        self.monitor_record_repo = monitor_record_repo
        self.logger = logger

    def get_response_time_metric_data(self, site_id: int, response_status: bool) -> List[MetricItem]:
        self.logger.info('Fetching response time metric data for site id %s', site_id)
        return self.monitor_record_repo.get_response_time_metric_data(site_id, response_status)

    def get_status_code_metric_data(self, site_id: int, response_status: bool) -> List[MetricItem]:
        self.logger.info('Fetching status code metric data for site id %s', site_id)
        return self.monitor_record_repo.get_status_code_metric_data(site_id, response_status)

    def get_content_matching_metric_data(self, site_id: int, response_status: bool) -> List[MetricItem]:
        self.logger.info('Fetching content matching metric data for site id %s', site_id)
        return self.monitor_record_repo.get_content_matching_metric_data(site_id, response_status)

    @classmethod
    def create(cls):
        db_connection = psycopg.connect(
            user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), dbname=os.getenv('DB_NAME')
        )
        monitor_record_repo = MonitorRecordRepo.create(db_connection)

        return cls(
            monitor_record_repo,
            getLogger(__name__)
        )
