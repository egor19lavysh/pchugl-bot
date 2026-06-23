from aiogram.fsm.state import State, StatesGroup


class PlayerStates(StatesGroup):
    title = State()
    nickname = State()
    tg_tag = State()
    level = State()
    account_strength = State()
    language = State()
    sieges_league = State()
    requirements_hydra = State()
    requirements_himera = State()
    requirements_lkv = State()
    photo = State()
    final = State()

class UpdatePlayerStates(StatesGroup):
    choice = State()
    title = State()
    nickname = State()
    tg_tag = State()
    level = State()
    account_strength = State()
    language = State()
    sieges_league = State()
    requirements_hydra = State()
    requirements_himera = State()
    requirements_lkv = State()
    photo = State()

class DeletePlayerStates(StatesGroup):
    confirm = State()