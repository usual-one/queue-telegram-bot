from __future__ import annotations

import enum


class UserStateValue(str, enum.Enum):
    NONE = 'none'
    EVENT_NAME_CREATING = 'event_name_creating'
    EVENT_TIME_CREATING = 'event_time_creating'
    QUEUE_TIME_CREATING = 'queue_time_creating'

class UserState:

    def __init__(self, value: UserStateValue, params: dict[str]) -> None:
        self.value = value
        self.params = params

    def from_dict(dictionary: dict) -> UserState:
        return UserState(value=dictionary['value'],
                         params=dictionary['params'])
