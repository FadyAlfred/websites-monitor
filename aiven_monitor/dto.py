from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Union


class MatchedContentEnum(Enum):
    MATCHED = 'matched'
    UNMATCHED = 'unmatched'
    NO_REGEX = 'no_regex'


class MetricItemTypeEnum(Enum):
    RESPONSE_TIME = 'response_time'
    STATUS_CODE = 'status_code'
    MATCHED_CONTENT = 'matched_content'


@dataclass
class Website:
    url: str
    created_at: Optional[datetime] = None
    regex: Optional[str] = None
    id: Optional[int] = None


@dataclass
class MonitorRecord:
    site_id: int
    response_time: float
    status_code: str
    is_content_matched: MatchedContentEnum
    created_at: Optional[datetime] = None
    id: Optional[int] = None

    def as_dict(self):
        result = self.__dict__
        result['is_content_matched'] = self.is_content_matched.value

        return result


@dataclass
class MetricItem:
    created_at: datetime
    value: Union[float | str | bool]
    type: MetricItemTypeEnum
