from logging import Logger
from unittest import TestCase
from unittest.mock import call, MagicMock, Mock

from kafka import KafkaConsumer

from aiven_monitor.dto import MatchedContentEnum, MonitorRecord
from aiven_monitor.monitor.monitor_consumer import MonitorConsumer
from aiven_monitor.repo import MonitorRecordRepo, WebsiteRepo
from tests.utils import generate_fake_website


class TestMonitorConsumer(TestCase):
    def setUp(self):
        self._fake_kafka_consumer = MagicMock(spec=KafkaConsumer)
        self._fake_website_repo = MagicMock(spec=WebsiteRepo)
        self._fake_monitor_record_repo = MagicMock(spec=MonitorRecordRepo)
        self._fake_logger = MagicMock(spec=Logger)
        self._monitor_consumer = MonitorConsumer(
            self._fake_kafka_consumer, self._fake_website_repo, self._fake_monitor_record_repo, self._fake_logger, False
        )

        self._fake_website = generate_fake_website()

        self._mock_manager = Mock()
        self._mock_manager.attach_mock(self._fake_kafka_consumer, 'fake_kafka_producer')
        self._mock_manager.attach_mock(self._fake_website_repo, 'fake_website_repo')
        self._mock_manager.attach_mock(self._fake_monitor_record_repo, 'fake_monitor_record_repo')
        self._mock_manager.attach_mock(self._fake_logger, 'fake_logger')

    def test_run_consumer(self):
        self._monitor_consumer.run_consumer()

        expected_calls = [
            call.fake_kafka_producer.poll(),
            call.fake_kafka_producer.poll().values(),
            call.fake_kafka_producer.poll().values().__iter__()
        ]

        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_handle_monitor_matched_content(self):
        message_dict = {
            'site_id': self._fake_website.id,
            'response_time': 0.01,
            'status_code': '200',
            'is_content_matched': MatchedContentEnum.MATCHED
        }

        self._monitor_consumer.handle_monitor(message_dict)

        expected_calls = [
            call.fake_monitor_record_repo.add(
                MonitorRecord(
                    site_id=1, response_time=0.01, status_code='200', is_content_matched=MatchedContentEnum.MATCHED,
                    created_at=None, id=None
                )
            )
        ]

        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_handle_monitor_unmatched_content(self):
        message_dict = {
            'site_id': self._fake_website.id,
            'response_time': 0.01,
            'status_code': '200',
            'is_content_matched': MatchedContentEnum.UNMATCHED
        }

        self._monitor_consumer.handle_monitor(message_dict)

        expected_calls = [
            call.fake_monitor_record_repo.add(
                MonitorRecord(
                    site_id=1, response_time=0.01, status_code='200', is_content_matched=MatchedContentEnum.UNMATCHED,
                    created_at=None, id=None
                )
            )
        ]

        self.assertEqual(self._mock_manager.mock_calls, expected_calls)
