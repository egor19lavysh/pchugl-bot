from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                            ReplyKeyboardMarkup, KeyboardButton)


async def tg_tag() -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Подставить свой автоматически")],
        [KeyboardButton(text="Пропустить")],
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

async def language_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="RU", callback_data="lang_RU")],
        [InlineKeyboardButton(text="UA", callback_data="lang_UA")],
        [InlineKeyboardButton(text="EN", callback_data="lang_EN")],
        [InlineKeyboardButton(text="Другое", callback_data="lang_Другое")],
        [InlineKeyboardButton(text="Назад", callback_data="lang_back")],
    ])

    return kb

async def hydra_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 1В", callback_data="hydra_До 1В"), InlineKeyboardButton(text="4В", callback_data="hydra_4В")],
        [InlineKeyboardButton(text="8В", callback_data="hydra_8В"), InlineKeyboardButton(text="12В", callback_data="hydra_12В")],
        [InlineKeyboardButton(text="16В", callback_data="hydra_16В"), InlineKeyboardButton(text="20В", callback_data="hydra_20В")],
        [InlineKeyboardButton(text="24В", callback_data="hydra_24В"), InlineKeyboardButton(text="От 28В", callback_data="hydra_От 28В")],
        [InlineKeyboardButton(text="Назад", callback_data="hydra_back")],

    ])

    return kb

async def himera_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 1В", callback_data="himera_До 1В"), InlineKeyboardButton(text="4В", callback_data="himera_4В")],
        [InlineKeyboardButton(text="8В", callback_data="himera_8В"), InlineKeyboardButton(text="12В", callback_data="himera_12В")],
        [InlineKeyboardButton(text="16В", callback_data="himera_16В"), InlineKeyboardButton(text="20В", callback_data="himera_20В")],
        [InlineKeyboardButton(text="24В", callback_data="himera_24В"), InlineKeyboardButton(text="От 28В", callback_data="himera_От 28В")],
        [InlineKeyboardButton(text="Назад", callback_data="himera_back")],

    ])

    return kb

async def lkv_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 100К", callback_data="lkv_До 100К"), InlineKeyboardButton(text="200K", callback_data="lkv_200К")],
        [InlineKeyboardButton(text="300К", callback_data="lkv_300К"), InlineKeyboardButton(text="400K", callback_data="lkv_400К")],
        [InlineKeyboardButton(text="500К", callback_data="lkv_500К"), InlineKeyboardButton(text="600K", callback_data="lkv_600К")],
        [InlineKeyboardButton(text="700К", callback_data="lkv_700К"), InlineKeyboardButton(text="От 800К", callback_data="lkv_От 800К")],
        [InlineKeyboardButton(text="Назад", callback_data="lkv_back")],

    ])

    return kb

async def sieges_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 5", callback_data="sieges_До 5"), InlineKeyboardButton(text="6", callback_data="sieges_6")],
        [InlineKeyboardButton(text="7", callback_data="sieges_7"), InlineKeyboardButton(text="8", callback_data="sieges_8")],
        [InlineKeyboardButton(text="Назад", callback_data="sieges_back")]])
    return kb