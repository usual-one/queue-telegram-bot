import json
import os

from ..entities.user_state import UserState, UserStateValue


STATE_FILEPATH = 'data/states.json'

class StateService:

    def __init__(self) -> None:
        self.states = self.__load(STATE_FILEPATH)

    def __load(self, filepath: str) -> dict[UserState]:
        if not os.path.exists(filepath):
            return dict()

        with open(filepath) as fin:
            dictionary = json.load(fin)
            return { id: UserState.from_dict(dictionary[id]) for id in dictionary.keys() }

    def __save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as fout:
            json.dump(obj={ id: vars(self.states[id]) for id in self.states.keys() },
                      fp=fout)

    def set(self,
            user_id: int,
            state: UserStateValue,
            params: dict[str] = dict()) -> None:
        self.states[str(user_id)] = UserState(state, params)
        self.__save(STATE_FILEPATH)

    def get(self, user_id: int) -> UserState:
        return self.states.get(str(user_id))
