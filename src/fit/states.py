from aiogram.fsm.state import State, StatesGroup


class SeacrhFilter(StatesGroup):
    player_lang = State()
    player_hydra = State()
    player_himera = State()
    player_lkv = State()
    player_sieges = State()

    clan_lang = State()
    clan_hydra = State()
    clan_himera = State()
    clan_lkv = State()
    clan_sieges = State()


class FitChoice(StatesGroup):
    choice = State()
    browsing = State()


class ReviewStates(StatesGroup):
    score = State()
    text = State()