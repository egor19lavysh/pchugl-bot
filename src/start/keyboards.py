from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def register_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Я игрок", callback_data="player")],
        [InlineKeyboardButton(text="🛡 Я клан", callback_data="clan")]
    ])
    return keyboard