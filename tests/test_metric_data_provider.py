from datetime import datetime
from logging import Logger
from unittest import TestCase
from unittest.mock import call, MagicMock, Mock

from aiven_monitor.dto import MetricItem, MetricItemTypeEnum
from aiven_monitor.metric_data_provider import MetricDataProvider
from aiven_monitor.repo import MonitorRecordRepo


class TestMetricDataProvider(TestCase):
    def setUp(self):
        self._fake_monitor_record_repo = MagicMock(spec=MonitorRecordRepo)
        self._fake_logger = MagicMock(spec=Logger)
        self._metric_data_provider = MetricDataProvider(
            self._fake_monitor_record_repo, self._fake_logger
        )

        self._fake_response_time_metric_item = MetricItem(
            created_at=datetime.now(), value=0.1, type=MetricItemTypeEnum.RESPONSE_TIME
        )
        self._fake_status_code_metric_item = MetricItem(
            created_at=datetime.now(), value='200', type=MetricItemTypeEnum.STATUS_CODE
        )
        self._fake_content_matched_metric_item = MetricItem(
            created_at=datetime.now(), value=True, type=MetricItemTypeEnum.MATCHED_CONTENT
        )

        self._mock_manager = Mock()
        self._mock_manager.attach_mock(self._fake_monitor_record_repo, 'fake_monitor_record_repo')
        self._mock_manager.attach_mock(self._fake_logger, 'fake_logger')

    def test_get_response_time_metric_data__success(self) -> None:
        self._fake_monitor_record_repo.get_response_time_metric_data.return_value = [
            self._fake_response_time_metric_item
        ]

        actual_result = self._metric_data_provider.get_response_time_metric_data(1, True)

        expected_calls = [
            call.fake_logger.info('Fetching response time metric data for site id %s', 1),
            call.fake_monitor_record_repo.get_response_time_metric_data(1, True)
        ]

        self.assertEqual(actual_result, [self._fake_response_time_metric_item])
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_get_response_time_metric_data__fail(self) -> None:
        self._fake_monitor_record_repo.get_response_time_metric_data.return_value = [
            self._fake_response_time_metric_item
        ]

        actual_result = self._metric_data_provider.get_response_time_metric_data(1, False)

        expected_calls = [
            call.fake_logger.info('Fetching response time metric data for site id %s', 1),
            call.fake_monitor_record_repo.get_response_time_metric_data(1, False)
        ]

        self.assertEqual(actual_result, [self._fake_response_time_metric_item])
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_get_status_code_metric_data__success(self) -> None:
        self._fake_monitor_record_repo.get_status_code_metric_data.return_value = [
            self._fake_status_code_metric_item
        ]

        actual_result = self._metric_data_provider.get_status_code_metric_data(1, True)

        expected_calls = [
            call.fake_logger.info('Fetching status code metric data for site id %s', 1),
            call.fake_monitor_record_repo.get_status_code_metric_data(1, True)
        ]

        self.assertEqual(actual_result, [self._fake_status_code_metric_item])
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_get_status_code_metric_data__fail(self) -> None:
        self._fake_status_code_metric_item.value = '400'
        self._fake_monitor_record_repo.get_status_code_metric_data.return_value = [
            self._fake_status_code_metric_item
        ]

        actual_result = self._metric_data_provider.get_status_code_metric_data(1, False)

        expected_calls = [
            call.fake_logger.info('Fetching status code metric data for site id %s', 1),
            call.fake_monitor_record_repo.get_status_code_metric_data(1, False)
        ]

        self.assertEqual(actual_result, [self._fake_status_code_metric_item])
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_get_content_matched_metric_data__success(self) -> None:
        self._fake_monitor_record_repo.get_content_matching_metric_data.return_value = [
            self._fake_content_matched_metric_item
        ]

        actual_result = self._metric_data_provider.get_content_matching_metric_data(1, True)

        expected_calls = [
            call.fake_logger.info('Fetching content matching metric data for site id %s', 1),
            call.fake_monitor_record_repo.get_content_matching_metric_data(1, True)
        ]

        self.assertEqual(actual_result, [self._fake_content_matched_metric_item])
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_get_content_matched_metric_data__fail(self) -> None:
        self._fake_content_matched_metric_item.value = False
        self._fake_monitor_record_repo.get_content_matching_metric_data.return_value = [
            self._fake_status_code_metric_item
        ]

        actual_result = self._metric_data_provider.get_content_matching_metric_data(1, False)

        expected_calls = [
            call.fake_logger.info('Fetching content matching metric data for site id %s', 1),
            call.fake_monitor_record_repo.get_content_matching_metric_data(1, False)
        ]

        self.assertEqual(actual_result, [self._fake_status_code_metric_item])
        self.assertEqual(self._mock_manager.mock_calls, expected_calls)
