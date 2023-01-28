from datetime import datetime
from typing import List, Tuple

from aiven_monitor.dto import MatchedContentEnum, MonitorRecord, Website


def assert_mock_calls(actual: List[Tuple], expected: List[Tuple]) -> None:
    assert len(actual) == len(expected)
    for i in range(len(actual)):
        # Call is a tuple [name, args, kwargs]
        assert actual[i][0] == expected[i][0]
        assert actual[i][1] == expected[i][1]
        assert actual[i][2] == expected[i][2]


def generate_fake_website() -> Website:
    return Website(
        id=1, url='https://www.test.come', regex='[a-z]', created_at=datetime.now()
    )


def generate_fake_monitor_record() -> MonitorRecord:
    return MonitorRecord(
            site_id=1, response_time=0.12, status_code='200', is_content_matched=MatchedContentEnum.MATCHED,
            created_at=datetime.now(), id=1
        )
