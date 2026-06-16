from aiogram.fsm.state import State, StatesGroup


class ClanStates(StatesGroup):
    title = State()
    nickname = State()
    tg_tag = State()
    level = State()
    photo = State()
    language = State()
    sieges_league = State()
    requirements_hydra = State()
    requirements_himera = State()
    requirements_lkv = State()

class UpdateClanStates(StatesGroup):
    choice = State()
    title = State()
    nickname = State()
    tg_tag = State()
    level = State()
    photo = State()
    language = State()
    sieges_league = State()
    requirements_hydra = State()
    requirements_himera = State()
    requirements_lkv = State()

class DeleteClanStates(StatesGroup):
    confirm = State()