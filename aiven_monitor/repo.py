from logging import getLogger, Logger
from typing import List, Optional, Tuple

from psycopg.connection import Connection

from aiven_monitor.dto import MetricItem, MetricItemTypeEnum, MonitorRecord, Website


class WebsiteRepo:
    def __init__(self, db_connection: Connection, logger: Logger):
        self.db_connection = db_connection
        self.db_curser = db_connection.cursor()
        self.logger = logger

    @staticmethod
    def _map_to_website(record: Tuple) -> Website:
        # TODO this need some improvements
        return Website(
            id=record[0],
            url=record[1],
            regex=record[2],
            created_at=record[3],
        )

    def fetch(self, id: int) -> Optional[Website]:
        self.logger.info('Fetch website with id %s', id)
        record = self.db_curser.execute('SELECT * FROM websites WHERE id = %s', (id, ))
        return self._map_to_website(record) if record else None

    def fetch_all(self) -> List[Website]:
        self.logger.info('Fetch all websites')
        records = self.db_curser.execute('SELECT * FROM websites')
        result = []
        for record in records:
            result.append(self._map_to_website(record))

        return result

    def add(self, website: Website) -> None:
        self.logger.info('Insert the following website to database %s', website.__dict__)
        self.db_curser.execute(
            'INSERT INTO websites (url, regex) VALUES (%s, %s)', (website.url, website.regex)
        )
        self.db_connection.commit()

    @classmethod
    def create(cls, db_connection: Connection):
        return cls(db_connection, getLogger(__name__))


class MonitorRecordRepo:
    def __init__(self, db_connection: Connection, logger: Logger):
        self.db_connection = db_connection
        self.db_curser = db_connection.cursor()
        self.logger = logger

    @staticmethod
    def _get_status_code_filter(response_status: bool) -> str:
        if response_status:
            status_code_filter = "status_code LIKE '2__' OR status_code LIKE '3__'"
        else:
            status_code_filter = "status_code NOT LIKE '2__' OR status_code NOT LIKE '3__'"

        return status_code_filter

    @staticmethod
    def _map_to_metric_item(record: Tuple, metric_unit: MetricItemTypeEnum) -> MetricItem:
        # TODO this need some improvements
        return MetricItem(
            value=record[0],
            created_at=record[1],
            type=metric_unit
        )

    def add(self, monitor_record: MonitorRecord) -> None:
        self.logger.info('Insert the following monitor record to the database %s', monitor_record.__dict__)
        self.db_curser.execute(
            'INSERT INTO monitor_records (site_id, status_code, response_time, is_content_matched)'
            ' VALUES (%s, %s, %s, %s)',
            (monitor_record.site_id, monitor_record.status_code, monitor_record.response_time,
             monitor_record.is_content_matched)
        )
        self.db_connection.commit()

    def get_response_time_metric_data(self, site_id: int, response_status: bool) -> List[MetricItem]:
        status_code_filter = self._get_status_code_filter(response_status)
        records = self.db_curser.execute(
            f'SELECT response_time, created_at FROM monitor_records WHERE site_id = %s AND {status_code_filter}',
            (site_id, )
        )
        result = []
        for record in records:
            result.append(self._map_to_metric_item(record, MetricItemTypeEnum.RESPONSE_TIME))

        return result

    def get_status_code_metric_data(self, site_id: int, response_status: bool):
        status_code_filter = self._get_status_code_filter(response_status)
        records = self.db_curser.execute(
            f'SELECT status_code, created_at FROM monitor_records WHERE site_id = %s AND {status_code_filter}',
            (site_id,)
        )
        result = []
        for record in records:
            result.append(self._map_to_metric_item(record, MetricItemTypeEnum.STATUS_CODE))

        return result

    def get_content_matching_metric_data(self, site_id: int, response_status: bool):
        status_code_filter = self._get_status_code_filter(response_status)
        records = self.db_curser.execute(
            f'SELECT is_content_matched, created_at FROM monitor_records WHERE site_id = %s AND {status_code_filter}',
            (site_id,)
        )
        result = []
        for record in records:
            result.append(self._map_to_metric_item(record, MetricItemTypeEnum.MATCHED_CONTENT))

        return result

    @classmethod
    def create(cls, db_connection: Connection):
        return cls(db_connection, getLogger(__name__))
