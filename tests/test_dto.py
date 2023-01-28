from datetime import datetime
from unittest import TestCase

from aiven_monitor.dto import MatchedContentEnum, MetricItem, MetricItemTypeEnum, MonitorRecord, Website


class TestWebsite(TestCase):
    def setUp(self):
        self.current_date = datetime.now()
        self.url = 'https://www.test.come'

    def test_website_dict(self) -> None:
        website_dict = {'url': self.url, 'created_at': self.current_date, 'id': None, 'regex': None}
        website = Website(url=self.url, created_at=self.current_date)

        self.assertEqual(website_dict, website.__dict__)


class TestMonitorRecord(TestCase):
    def setUp(self):
        self.site_id = 1
        self.response_time = 0.892
        self.status_code = '200'
        self.is_content_matched = MatchedContentEnum.MATCHED

    def test_monitor_record_as_dict(self) -> None:
        monitor_record_dict = {
            'site_id': self.site_id, 'response_time': self.response_time, 'status_code': self.status_code,
            'is_content_matched': self.is_content_matched.value, 'id': None, 'created_at': None
        }
        monitor_record = MonitorRecord(
            site_id=self.site_id, response_time=self.response_time, status_code=self.status_code,
            is_content_matched=self.is_content_matched
        )

        self.assertEqual(monitor_record_dict, monitor_record.as_dict())


class TestMetricItem(TestCase):
    def setUp(self):
        self.created_at = datetime.now()
        self.value = 0.23
        self.unit = MetricItemTypeEnum.RESPONSE_TIME

    def test_metric_item_dict(self) -> None:
        metric_item_dict = {'created_at': self.created_at, 'value': self.value, 'type': self.unit}
        metric_item = MetricItem(created_at=self.created_at, value=self.value, type=self.unit)

        self.assertEqual(metric_item_dict, metric_item.__dict__)
