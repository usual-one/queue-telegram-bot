from __future__ import annotations

import enum


class UserStateValue(str, enum.Enum):
    NONE = 'none'
    EVENT_NAME_CREATING = 'event_name_creating'
    EVENT_TIME_CREATING = 'event_time_creating'
    QUEUE_TIME_CREATING = 'queue_time_creating'
