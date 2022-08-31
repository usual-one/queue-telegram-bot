import datetime


class Event:

    def __init__(self, name: str, time: datetime.datetime) -> None:
        self.name = name
        self.time = time
