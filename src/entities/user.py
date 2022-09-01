from __future__ import annotations

import telegram as tg

from .user_role import UserRole


class User:

    def __init__(self, name: str, role: UserRole) -> None:
        self.name = name
        self.role = role

    @staticmethod
    def from_tg_user(tg_user: tg.User, role: UserRole) -> User:
        return User(name=tg_user.full_name,
                    role=role)

    @staticmethod
    def from_dict(dictionary: dict) -> User:
        return User(name=dictionary['name'],
                    role=dictionary['role'])
