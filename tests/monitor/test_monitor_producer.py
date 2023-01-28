from logging import Logger
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, call, MagicMock, Mock, patch

from kafka import KafkaProducer

from aiven_monitor.dto import MatchedContentEnum, MonitorRecord
from aiven_monitor.monitor.monitor_producer import MonitorProducer
from aiven_monitor.repo import WebsiteRepo
from tests.utils import generate_fake_website


class TestMonitorProducer(IsolatedAsyncioTestCase):
    def setUp(self):
        self._fake_kafka_producer = MagicMock(spec=KafkaProducer)
        self._fake_website_repo = MagicMock(spec=WebsiteRepo)
        self._fake_logger = MagicMock(spec=Logger)
        self._monitor_producer = MonitorProducer(self._fake_kafka_producer, self._fake_website_repo, self._fake_logger)

        self._fake_website_repo.db_connection = MagicMock()
        self._fake_website = generate_fake_website()

        self._mock_manager = Mock()
        self._mock_manager.attach_mock(self._fake_kafka_producer, 'fake_kafka_producer')
        self._mock_manager.attach_mock(self._fake_website_repo, 'fake_website_repo')
        self._mock_manager.attach_mock(self._fake_logger, 'fake_logger')

    def test_run_producer(self):
        self._monitor_producer.run_producer()
        expected_calls = [
            call.fake_website_repo.fetch_all(),
            call.fake_website_repo.fetch_all().__iter__(),
            call.fake_kafka_producer.close(),
            call.fake_website_repo.db_connection.close()
        ]
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    @patch('time.perf_counter', return_value=1.0)
    @patch('aiohttp.ClientSession.get')
    async def test_run_health_check_matched_regex(self, client_session_mock: AsyncMock, _):
        client_session_mock.return_value.__aenter__.return_value.text.return_value = 'fake html page'
        client_session_mock.return_value.__aenter__.return_value.status = 200

        await self._monitor_producer._run_health_check([self._fake_website])

        expected_calls = [
            call.fake_logger.info('Run health check on %s', 'https://www.test.come'),
            call.fake_logger.info(
                'Send monitor record about website %s with following record %s', 'https://www.test.come',
                MonitorRecord(
                    site_id=1, response_time=0.0, status_code='200', is_content_matched=MatchedContentEnum.MATCHED,
                    created_at=None, id=None
                ).as_dict()
            ),
            call.fake_kafka_producer.send(
                None, (
                    b'{"site_id": 1, "response_time": 0.0, "status_code": "200", '
                    b'"is_content_matched": "matched", "created_at": null, "id": null}'
                )
            )
        ]

        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    @patch('time.perf_counter', return_value=1.0)
    @patch('aiohttp.ClientSession.get')
    async def test_run_health_check_unmatched_regex(self, client_session_mock: AsyncMock, _):
        client_session_mock.return_value.__aenter__.return_value.text.return_value = ''
        client_session_mock.return_value.__aenter__.return_value.status = 200

        await self._monitor_producer._run_health_check([self._fake_website])

        expected_calls = [
            call.fake_logger.info('Run health check on %s', 'https://www.test.come'),
            call.fake_logger.info(
                'Send monitor record about website %s with following record %s', 'https://www.test.come',
                MonitorRecord(
                    site_id=1, response_time=0.0, status_code='200', is_content_matched=MatchedContentEnum.UNMATCHED,
                    created_at=None, id=None
                ).as_dict()
            ),
            call.fake_kafka_producer.send(
                None, (
                    b'{"site_id": 1, "response_time": 0.0, "status_code": "200", '
                    b'"is_content_matched": "unmatched", "created_at": null, "id": null}'
                )
            )
        ]
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)
