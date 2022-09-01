import json
import os

from ..entities.user_state import UserStateValue


STATE_FILEPATH = 'data/states.json'

class StateService:

    def __init__(self) -> None:
        self.states = self.__load(STATE_FILEPATH)

    def __load(self, filepath: str) -> dict[UserStateValue]:
        if not os.path.exists(filepath):
            return dict()

        with open(filepath) as fin:
            return json.load(fin)

    def __save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as fout:
            json.dump(obj=self.states, fp=fout)

    def set(self, user_id: int, state: UserStateValue) -> None:
        self.states[str(user_id)] = state
        self.__save(STATE_FILEPATH)

    def get(self, user_id: int) -> UserStateValue:
        return self.states.get(str(user_id))
