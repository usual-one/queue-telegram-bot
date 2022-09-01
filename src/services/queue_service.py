from collections.abc import Callable
from datetime import datetime
import json
import os

from ..entities.queue import Queue
from ..entities.event import Event


QUEUE_FILEPATH = 'data/queues.json'

class QueueService:

    def __init__(self,
                 date_format: str,
                 queue_create_cb: Callable = lambda queue: None):
        self.__date_format = date_format
        self.__queue_create_cb = queue_create_cb

        self.__queues = self.__load(QUEUE_FILEPATH)

    def create_queue(self,
                     event_name: str,
                     event_time: str,
                     queue_time: str) -> None:
        event = Event(event_name, datetime.strptime(event_time, self.__date_format))
        queue = Queue(event, datetime.strptime(queue_time, self.__date_format))
        self.__queues.append(queue)
        self.__save(QUEUE_FILEPATH)

        self.__queue_create_cb(queue)

    def is_valid_datetime(self, dt: str) -> bool:
        try:
            datetime.strptime(dt, self.__date_format)
        except:
            return False
        return True

    def __load(self, filepath: str) -> list[Queue]:
        if not os.path.exists(filepath):
            return []

        with open(filepath) as fin:
            return [Queue.from_dict(dictionary, self.__date_format) for dictionary in json.load(fin)]

    def __save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as fout:
            json.dump(obj=[queue.to_dict(self.__date_format) for queue in self.__queues],
                      fp=fout)
