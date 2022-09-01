from __future__ import annotations
from datetime import datetime

from .event import Event


class Queue:

    def __init__(self, event: Event, start_time: datetime) -> None:
        self.event = event
        self.__start_time = start_time
        self.members = []

    def get_start_time(self, format: str) -> str:
        return self.__start_time.strftime(format)

    @staticmethod
    def from_dict(dictionary: dict, date_format: str) -> Queue:
        return Queue(event=Event.from_dict(dictionary['event'], date_format),
                     start_time=datetime.strptime(dictionary['start_time'], date_format))

    def to_dict(self, date_format: str) -> dict:
        return { 'event': self.event.to_dict(date_format),
                'start_time': self.get_start_time(date_format) }

