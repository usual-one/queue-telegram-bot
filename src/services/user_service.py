import json
import os
import pathlib

import telegram as tg

from ..entities.user import User
from ..entities.user_role import UserRole


USER_FILEPATH = 'data/users.json'

class UserService:

    def __init__(self) -> None:
        self.users = self.__load(USER_FILEPATH)

    def append(self, tg_user: tg.User) -> None:
        if self.has(tg_user.id):
            return

        user = User.from_tg_user(tg_user, UserRole.USER)
        self.users[str(tg_user.id)] = user
        self.__save(USER_FILEPATH)

    def has(self, id: int) -> bool:
        return any([user_id == str(id) for user_id in self.users.keys()])

    def get(self, id: int) -> User:
        return self.users[str(id)]

    def __load(self, filepath: str) -> list[User]:
        if not os.path.exists(filepath):
            return dict()

        with open(filepath) as fin:
            dictionary = json.load(fin)
            return {id: User.from_dict(dictionary[id]) for id in dictionary.keys()}

    def __save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as fout:
            json.dump(obj={id: vars(self.users[id]) for id in self.users.keys()},
                      fp=fout)

