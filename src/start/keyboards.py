from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def register_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Я игрок", callback_data="create_player")],
        [InlineKeyboardButton(text="🛡 Я клан", callback_data="create_clan")]
    ])
    return keyboard

async def profiles_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Анкеты игрока", callback_data="player")],
        [InlineKeyboardButton(text="🛡 Анкеты клана", callback_data="clan")]
    ])
    return keyboard