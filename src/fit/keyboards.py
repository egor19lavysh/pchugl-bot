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
        [InlineKeyboardButton(text="Оставить отзыв", callback_data=f"review_{entity}_{profile_id}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"fit_list")]

    ])

async def review_back(profile_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться к анкете", callback_data=f"fit_profile_{profile_id}")]
    ])

async def review_score_kb(profile_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1⭐️", callback_data=f"review_score_{profile_id}_1")],
            [InlineKeyboardButton(text="2⭐️", callback_data=f"review_score_{profile_id}_2")],
            [InlineKeyboardButton(text="3⭐️", callback_data=f"review_score_{profile_id}_3")],
            [InlineKeyboardButton(text="4⭐️", callback_data=f"review_score_{profile_id}_4")],
            [InlineKeyboardButton(text="5⭐️", callback_data=f"review_score_{profile_id}_5")],
        
        [InlineKeyboardButton(text="Вернуться к анкете", callback_data=f"fit_profile_{profile_id}")],
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
        InlineKeyboardButton(text="Вернуться к анкете", callback_data=f"fit_profile_{profile_id}"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def back_to_search() -> InlineKeyboardButton:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="fit")]
    ])


async def profiles_page_kb(profiles: list, page: int = 0) -> InlineKeyboardMarkup:
    """
    Build InlineKeyboardMarkup for profiles: 2 buttons per row, 8 rows (16 items per page).
    Adds Prev/Next navigation buttons with page indicated in callback_data.
    """
    per_page = 16
    start = page * per_page
    page_items = profiles[start:start + per_page]

    builder = InlineKeyboardBuilder()

    for p in page_items:
        title = getattr(p, "nickname", None) or getattr(p, "name", None) or str(p)
        callback = f"fit_profile_{p.id}"
        builder.add(InlineKeyboardButton(text=title, callback_data=callback))

    builder.adjust(2)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀️Назад", callback_data=f"fit_prev_{page - 1}"))
    if start + per_page < len(profiles):
        nav_buttons.append(InlineKeyboardButton(text="Дальше▶️", callback_data=f"fit_next_{page + 1}"))

    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(InlineKeyboardButton(text="Назад к поиску", callback_data="fit"))

    return builder.as_markup()


