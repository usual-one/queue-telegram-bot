from __future__ import annotations
from datetime import datetime


class Event:

    def __init__(self, name: str, time: datetime) -> None:
        self.name = name
        self.__time = time

    def get_time(self, format: str) -> str:
        return self.__time.strftime(format)

    @staticmethod
    def from_dict(dictionary: dict[str], date_format: str) -> Event:
        return Event(name=dictionary['name'],
                     time=datetime.strptime(dictionary['time'], date_format))

    def to_dict(self, date_format: str) -> dict[str]:
        return { 'name': self.name, 'time': self.get_time(date_format) }
