from logging import Logger
from unittest import TestCase
from unittest.mock import call, MagicMock, Mock

from psycopg.connection import Connection

from aiven_monitor.dto import MetricItem, MetricItemTypeEnum, Website
from aiven_monitor.repo import MonitorRecordRepo, WebsiteRepo
from tests.utils import assert_mock_calls, generate_fake_monitor_record, generate_fake_website


class TestWebsiteRepo(TestCase):
    def setUp(self):
        self._fake_db_connection = MagicMock(spec=Connection)
        self._fake_logger = MagicMock(spec=Logger)
        self._website_repo = WebsiteRepo(self._fake_db_connection, self._fake_logger)

        self._fake_website = generate_fake_website()
        self._fake_db_record = (
            self._fake_website.id, self._fake_website.url, self._fake_website.regex, self._fake_website.created_at
        )

        self._mock_manager = Mock()
        self._mock_manager.attach_mock(self._fake_db_connection, 'fake_db_connection')
        self._mock_manager.attach_mock(self._fake_logger, 'fake_logger')

    def test_fetch(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = self._fake_db_record

        actual_result = self._website_repo.fetch(self._fake_website.id)

        expected_calls = [
            call.fake_logger.info('Fetch website with id %s', self._fake_website.id),
            call.fake_db_connection.cursor().execute('SELECT * FROM websites WHERE id = %s', (self._fake_website.id,))
        ]

        self.assertEqual(actual_result, self._fake_website)
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_fetch_empty(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = None

        actual_result = self._website_repo.fetch(self._fake_website.id)

        expected_calls = [
            call.fake_logger.info('Fetch website with id %s', self._fake_website.id),
            call.fake_db_connection.cursor().execute('SELECT * FROM websites WHERE id = %s', (self._fake_website.id,))
        ]

        self.assertEqual(actual_result, None)
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_fetch_all(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = [self._fake_db_record]

        actual_result = self._website_repo.fetch_all()

        expected_calls = [
            call.fake_logger.info('Fetch all websites'),
            call.fake_db_connection.cursor().execute('SELECT * FROM websites')
        ]

        self.assertEqual(actual_result, [self._fake_website])
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_fetch_all_empty(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = []

        actual_result = self._website_repo.fetch_all()

        expected_calls = [
            call.fake_logger.info('Fetch all websites'),
            call.fake_db_connection.cursor().execute('SELECT * FROM websites')
        ]

        self.assertEqual(actual_result, [])
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_add(self):
        website_to_add = Website(url='https://www.fake.come', regex=self._fake_website.regex)
        self._website_repo.add(website_to_add)

        expected_calls = [
            call.fake_logger.info(
                'Insert the following website to database %s',
                {'url': website_to_add.url, 'created_at': None, 'regex': website_to_add.regex, 'id': None}
            ),
            call.fake_db_connection.cursor().execute(
                'INSERT INTO websites (url, regex) VALUES (%s, %s)',
                (website_to_add.url, website_to_add.regex)
            ),
            call.fake_db_connection.commit()
        ]

        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)


class TestMonitorRecordRepo(TestCase):
    def setUp(self):
        self._fake_db_connection = MagicMock(spec=Connection)
        self._fake_logger = MagicMock(spec=Logger)
        self._monitor_repo = MonitorRecordRepo(self._fake_db_connection, self._fake_logger)

        self._fake_monitor_record = generate_fake_monitor_record()
        self._fake_db_record = (
            self._fake_monitor_record.id,
            self._fake_monitor_record.site_id, self._fake_monitor_record.status_code,
            self._fake_monitor_record.response_time, self._fake_monitor_record.is_content_matched
        )

        self._mock_manager = Mock()
        self._mock_manager.attach_mock(self._fake_db_connection, 'fake_db_connection')
        self._mock_manager.attach_mock(self._fake_logger, 'fake_logger')

    def test_add(self):
        self._monitor_repo.add(self._fake_monitor_record)

        expected_calls = [
            call.fake_logger.info(
                'Insert the following monitor record to the database %s',
                {'site_id': self._fake_monitor_record.site_id, 'response_time': self._fake_monitor_record.response_time,
                 'status_code': self._fake_monitor_record.status_code,
                 'is_content_matched': self._fake_monitor_record.is_content_matched,
                 'created_at': self._fake_monitor_record.created_at, 'id': self._fake_monitor_record.id}
            ),
            call.fake_db_connection.cursor().execute(
                'INSERT INTO monitor_records (site_id, status_code, response_time, is_content_matched) '
                'VALUES (%s, %s, %s, %s)',
                (self._fake_monitor_record.site_id, self._fake_monitor_record.status_code,
                 self._fake_monitor_record.response_time, self._fake_monitor_record.is_content_matched)
            ),
            call.fake_db_connection.commit()
        ]
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_get_response_time_metric_data__success(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = [(
            self._fake_monitor_record.response_time, self._fake_monitor_record.created_at
        )]

        actual_result = self._monitor_repo.get_response_time_metric_data(1, True)

        expected_calls = [
            call.fake_db_connection.cursor().execute(
                'SELECT response_time, created_at FROM monitor_records WHERE site_id = %s AND '
                "status_code LIKE '2__' OR status_code LIKE '3__'",
                (self._fake_monitor_record.site_id,)),
        ]

        self.assertEqual(
            actual_result,
            [MetricItem(
                created_at=self._fake_monitor_record.created_at, value=self._fake_monitor_record.response_time,
                type=MetricItemTypeEnum.RESPONSE_TIME
            )]
        )
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_get_response_time_metric_data__fail(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = [(
            self._fake_monitor_record.response_time, self._fake_monitor_record.created_at
        )]

        actual_result = self._monitor_repo.get_response_time_metric_data(1, False)

        expected_calls = [
            call.fake_db_connection.cursor().execute(
                'SELECT response_time, created_at FROM monitor_records WHERE site_id = %s AND '
                "status_code NOT LIKE '2__' OR status_code NOT LIKE '3__'",
                (self._fake_monitor_record.site_id,)),
        ]

        self.assertEqual(
            actual_result,
            [MetricItem(
                created_at=self._fake_monitor_record.created_at, value=self._fake_monitor_record.response_time,
                type=MetricItemTypeEnum.RESPONSE_TIME
            )]
        )
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_get_status_code_metric_data__success(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = [(
            self._fake_monitor_record.response_time, self._fake_monitor_record.created_at
        )]

        actual_result = self._monitor_repo.get_status_code_metric_data(1, True)

        expected_calls = [
            call.fake_db_connection.cursor().execute(
                'SELECT status_code, created_at FROM monitor_records WHERE site_id = %s AND '
                "status_code LIKE '2__' OR status_code LIKE '3__'",
                (self._fake_monitor_record.site_id,)),
        ]

        self.assertEqual(
            actual_result,
            [MetricItem(
                created_at=self._fake_monitor_record.created_at, value=self._fake_monitor_record.response_time,
                type=MetricItemTypeEnum.STATUS_CODE
            )]
        )
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_get_status_code_metric_data__fail(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = [(
            self._fake_monitor_record.response_time, self._fake_monitor_record.created_at
        )]

        actual_result = self._monitor_repo.get_status_code_metric_data(1, False)

        expected_calls = [
            call.fake_db_connection.cursor().execute(
                'SELECT status_code, created_at FROM monitor_records WHERE site_id = %s AND '
                "status_code NOT LIKE '2__' OR status_code NOT LIKE '3__'",
                (self._fake_monitor_record.site_id,)),
        ]

        self.assertEqual(
            actual_result,
            [MetricItem(
                created_at=self._fake_monitor_record.created_at, value=self._fake_monitor_record.response_time,
                type=MetricItemTypeEnum.STATUS_CODE
            )]
        )
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_get_content_matching_metric_data__success(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = [(
            self._fake_monitor_record.response_time, self._fake_monitor_record.created_at
        )]

        actual_result = self._monitor_repo.get_content_matching_metric_data(1, True)

        expected_calls = [
            call.fake_db_connection.cursor().execute(
                'SELECT is_content_matched, created_at FROM monitor_records WHERE site_id = %s AND '
                "status_code LIKE '2__' OR status_code LIKE '3__'",
                (self._fake_monitor_record.site_id,)),
        ]

        self.assertEqual(
            actual_result,
            [MetricItem(
                created_at=self._fake_monitor_record.created_at, value=self._fake_monitor_record.response_time,
                type=MetricItemTypeEnum.MATCHED_CONTENT
            )]
        )
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)

    def test_get_content_matching_metric_data__fail(self):
        self._fake_db_connection.cursor.return_value.execute.return_value = [(
            self._fake_monitor_record.response_time, self._fake_monitor_record.created_at
        )]

        actual_result = self._monitor_repo.get_content_matching_metric_data(1, False)

        expected_calls = [
            call.fake_db_connection.cursor().execute(
                'SELECT is_content_matched, created_at FROM monitor_records WHERE site_id = %s AND '
                "status_code NOT LIKE '2__' OR status_code NOT LIKE '3__'",
                (self._fake_monitor_record.site_id,)),
        ]

        self.assertEqual(
            actual_result,
            [MetricItem(
                created_at=self._fake_monitor_record.created_at, value=self._fake_monitor_record.response_time,
                type=MetricItemTypeEnum.MATCHED_CONTENT
            )]
        )
        assert_mock_calls(self._mock_manager.mock_calls, expected_calls)
