import telegram as tg

from ..entities.user import User
from ..entities.user_role import UserRole


class UserService:

    def __init__(self) -> None:
        self.users: list[User] = []

    def append(self, tg_user: tg.User) -> None:
        if (self.has(tg_user.id)):
            return

        user = User(tg_user, UserRole.USER)
        self.users.append(user)

    def has(self, id: int) -> bool:
        for user in self.users:
            if (user.id == id):
                return True
        return False
