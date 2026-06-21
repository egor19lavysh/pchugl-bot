from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def search_type() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Все анкеты", callback_data="search_all")],
        [InlineKeyboardButton(text="Фильтр", callback_data="search_filter")]
    ])

async def fit_action() -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Назад"), KeyboardButton(text="Дальше")],
        [KeyboardButton(text="Выйти")]
    ]

    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

async def profile_action(entity: str, profile_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Смотреть отзывы", callback_data=f"reviews_{entity}_{profile_id}")],
        [InlineKeyboardButton(text="Оставить отзыв", callback_data=f"review_{entity}_{profile_id}")]

    ])

async def review_control_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться к анкете", callback_data="review_back")]
    ])

async def review_pagination_kb(entity: str, profile_id: int, index: int, total: int) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    if index > 0:
        row.append(InlineKeyboardButton(text="Предыдущий", callback_data=f"reviews_prev_{entity}_{profile_id}_{index - 1}"))
    if index < total - 1:
        row.append(InlineKeyboardButton(text="Следующий", callback_data=f"reviews_next_{entity}_{profile_id}_{index + 1}"))
    if row:
        buttons.append(row)
    buttons.append([
        InlineKeyboardButton(text="Вернуться к анкете", callback_data="review_back"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def back_to_search() -> InlineKeyboardButton:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="fit")]
    ])