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