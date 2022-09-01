import json


LOCALE_FILE = 'assets/locale.json'

class LocaleService:

    def __init__(self) -> None:
        with open(LOCALE_FILE) as fin:
            self.__dict: dict[str] = json.load(fin)

    def get_by_key(self, key: str) -> str:
        return self.__dict[key]

    def get_with_args(self, key: str, *args) -> str:
        return self.__dict[key].format(*args)
