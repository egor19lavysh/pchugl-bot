from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                            ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.player.models import Player


async def tg_tag() -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Подставить свой автоматически")],
        [KeyboardButton(text="Пропустить")],
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

async def language_kb(skip: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="RU", callback_data="lang_RU")],
        [InlineKeyboardButton(text="UA", callback_data="lang_UA")],
        [InlineKeyboardButton(text="EN", callback_data="lang_EN")],
        [InlineKeyboardButton(text="Другое", callback_data="lang_Другое")],
        [InlineKeyboardButton(text="Назад", callback_data="lang_Назад")],
    ])

    if skip:
        kb.inline_keyboard.insert(4, [InlineKeyboardButton(text="Пропустить", callback_data="lang_Пропустить")])

    return kb

async def hydra_kb(skip: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 1В", callback_data="hydra_1"), InlineKeyboardButton(text="От 1В", callback_data="hydra_2")],
        [InlineKeyboardButton(text="От 4В", callback_data="hydra_4"), InlineKeyboardButton(text="От 8В", callback_data="hydra_8")],
        [InlineKeyboardButton(text="От 12В", callback_data="hydra_12"), InlineKeyboardButton(text="От 16В", callback_data="hydra_16")],
        [InlineKeyboardButton(text="От 20В", callback_data="hydra_20"), InlineKeyboardButton(text="От 24В", callback_data="hydra_24")],
        [InlineKeyboardButton(text="Назад", callback_data="hydra_Назад")],

    ])

    if skip:
        kb.inline_keyboard.insert(4, [InlineKeyboardButton(text="Пропустить", callback_data="lang_Пропустить")])


    return kb

async def himera_kb(skip: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 1В", callback_data="himera_1"), InlineKeyboardButton(text="От 1В", callback_data="himera_2")],
        [InlineKeyboardButton(text="От 4В", callback_data="himera_4"), InlineKeyboardButton(text="От 8В", callback_data="himera_8")],
        [InlineKeyboardButton(text="От 12В", callback_data="himera_12"), InlineKeyboardButton(text="От 16В", callback_data="himera_16")],
        [InlineKeyboardButton(text="От 20В", callback_data="himera_20"), InlineKeyboardButton(text="От 24В", callback_data="himera_24")],
        [InlineKeyboardButton(text="Назад", callback_data="himera_Назад")],

    ])

    if skip:
        kb.inline_keyboard.insert(4, [InlineKeyboardButton(text="Пропустить", callback_data="lang_Пропустить")])


    return kb

async def lkv_kb(skip: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 100К", callback_data="lkv_100"), InlineKeyboardButton(text="От 100К", callback_data="lkv_101")],
        [InlineKeyboardButton(text="От 200K", callback_data="lkv_200"), InlineKeyboardButton(text="От 300К", callback_data="lkv_300")],
        [InlineKeyboardButton(text="От 400K", callback_data="lkv_400"), InlineKeyboardButton(text="От 500К", callback_data="lkv_500")],
        [InlineKeyboardButton(text="От 600K", callback_data="lkv_600"), InlineKeyboardButton(text="От 700К", callback_data="lkv_700")],
        [InlineKeyboardButton(text="Назад", callback_data="lkv_Назад")],

    ])

    if skip:
        kb.inline_keyboard.insert(4, [InlineKeyboardButton(text="Пропустить", callback_data="lang_Пропустить")])


    return kb

async def sieges_kb(skip: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 5", callback_data="sieges_5"), InlineKeyboardButton(text="От 6", callback_data="sieges_6")],
        [InlineKeyboardButton(text="От 7", callback_data="sieges_7"), InlineKeyboardButton(text="8", callback_data="sieges_8")],
        [InlineKeyboardButton(text="Назад", callback_data="sieges_Назад")]])
    
    if skip:
        kb.inline_keyboard.insert(2, [InlineKeyboardButton(text="Пропустить", callback_data="lang_Пропустить")])
    
    return kb

async def photo_kb() -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Пропустить")],
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

async def final_action_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сохранить анкету", callback_data="final_1")],
        [InlineKeyboardButton(text="Сохранить и опубликовать анкету", callback_data="final_2")]
    ])

async def back_kb() -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

async def get_user_player_profiles(players: list[Player]) -> InlineKeyboardMarkup:
    """
    Клавиатура, которая отдает список профилей пользователя как игрока
    """
    builder = InlineKeyboardBuilder()

    for player in players:
        builder.add(
            InlineKeyboardButton(text=player.title, callback_data=f"player_{player.id}")
        )
    
    builder.add(
        InlineKeyboardButton(text="Опубликовать все", callback_data=f"publish_players")
    )

    builder.add(
        InlineKeyboardButton(text="Назад", callback_data=f"player_Назад")
    )

    builder.adjust(1)

    return builder.as_markup()

async def get_player_profile_actions(player_id: int, is_published: bool = False) -> InlineKeyboardMarkup:
    """
    Отдает возможные действия с анкетой
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Опубликовать", callback_data=f"publish_player_{player_id}") if not is_published else InlineKeyboardButton(text="Снять с публикации", callback_data=f"unpublish_player_{player_id}") ],
        [InlineKeyboardButton(text="Изменить", callback_data=f"update_player_{player_id}")],
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_player_{player_id}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"back_from_profile")],

    ])

    return kb

async def get_confirm_delete() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="confirm_delete_player_Да"), InlineKeyboardButton(text="Нет", callback_data="confirm_delete_player_Нет")]
    ])

    return kb

async def back_to_player(player_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"player_{player_id}")]
    ])
    return kb

async def back_to_players() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"player")]
    ])
    return kb

title = "Название анкеты"
nick = "Ник"
tg = "Тг юзернейм"
level = "Уровень"
account_strength = "Сила аккаунта"
lang = "Язык"
hydra = "Гидра"
himera = "Химера"
lkv = "ЛКВ"
sieges = "Осады"
photo = "Картинка"
async def get_player_fields_for_update() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title, callback_data="patch_player_field_" + title)],
        [InlineKeyboardButton(text=nick, callback_data="patch_player_field_" + nick)],
        [InlineKeyboardButton(text=tg, callback_data="patch_player_field_" + tg)],
        [InlineKeyboardButton(text=level, callback_data="patch_player_field_" + level)],
        [InlineKeyboardButton(text=account_strength, callback_data="patch_player_field_" + account_strength)],
        [InlineKeyboardButton(text=lang, callback_data="patch_player_field_" + lang)],
        [InlineKeyboardButton(text=hydra, callback_data="patch_player_field_" + hydra)],
        [InlineKeyboardButton(text=himera, callback_data="patch_player_field_" + himera)],
        [InlineKeyboardButton(text=lkv, callback_data="patch_player_field_" + lkv)],
        [InlineKeyboardButton(text=sieges, callback_data="patch_player_field_" + sieges)],
        [InlineKeyboardButton(text=photo, callback_data="patch_player_field_" + photo)],
        [InlineKeyboardButton(text="Назад", callback_data="patch_player_field_Назад")],
    ])

    return kb

async def publish_again(player_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Опубликовать снова", callback_data=f"publish_player_{player_id}")]
        ]
    )

    return kb