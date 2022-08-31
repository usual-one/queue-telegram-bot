import datetime

from .event import Event


class Queue:

    def __init__(self, event: Event, start_time: datetime.datetime) -> None:
        self.event = event
        self.start_time = start_time
        self.members = []
