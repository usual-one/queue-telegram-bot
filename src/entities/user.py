import telegram as tg

from .user_role import UserRole


class User:

    def __init__(self, tg_user: tg.User, role: UserRole) -> None:
        self.id = tg_user.id
        self.name = tg_user.full_name
        self.role = role
