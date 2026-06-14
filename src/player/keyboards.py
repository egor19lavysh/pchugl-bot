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

async def language_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="RU", callback_data="lang_RU")],
        [InlineKeyboardButton(text="UA", callback_data="lang_UA")],
        [InlineKeyboardButton(text="EN", callback_data="lang_EN")],
        [InlineKeyboardButton(text="Другое", callback_data="lang_Другое")],
        [InlineKeyboardButton(text="Назад", callback_data="lang_Назад")],
    ])

    return kb

async def hydra_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 1В", callback_data="hydra_До 1В"), InlineKeyboardButton(text="4В", callback_data="hydra_4В")],
        [InlineKeyboardButton(text="8В", callback_data="hydra_8В"), InlineKeyboardButton(text="12В", callback_data="hydra_12В")],
        [InlineKeyboardButton(text="16В", callback_data="hydra_16В"), InlineKeyboardButton(text="20В", callback_data="hydra_20В")],
        [InlineKeyboardButton(text="24В", callback_data="hydra_24В"), InlineKeyboardButton(text="От 28В", callback_data="hydra_От 28В")],
        [InlineKeyboardButton(text="Назад", callback_data="hydra_Назад")],

    ])

    return kb

async def himera_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 1В", callback_data="himera_До 1В"), InlineKeyboardButton(text="4В", callback_data="himera_4В")],
        [InlineKeyboardButton(text="8В", callback_data="himera_8В"), InlineKeyboardButton(text="12В", callback_data="himera_12В")],
        [InlineKeyboardButton(text="16В", callback_data="himera_16В"), InlineKeyboardButton(text="20В", callback_data="himera_20В")],
        [InlineKeyboardButton(text="24В", callback_data="himera_24В"), InlineKeyboardButton(text="От 28В", callback_data="himera_От 28В")],
        [InlineKeyboardButton(text="Назад", callback_data="himera_Назад")],

    ])

    return kb

async def lkv_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 100К", callback_data="lkv_До 100К"), InlineKeyboardButton(text="200K", callback_data="lkv_200К")],
        [InlineKeyboardButton(text="300К", callback_data="lkv_300К"), InlineKeyboardButton(text="400K", callback_data="lkv_400К")],
        [InlineKeyboardButton(text="500К", callback_data="lkv_500К"), InlineKeyboardButton(text="600K", callback_data="lkv_600К")],
        [InlineKeyboardButton(text="700К", callback_data="lkv_700К"), InlineKeyboardButton(text="От 800К", callback_data="lkv_От 800К")],
        [InlineKeyboardButton(text="Назад", callback_data="lkv_Назад")],

    ])

    return kb

async def sieges_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 5", callback_data="sieges_До 5"), InlineKeyboardButton(text="6", callback_data="sieges_6")],
        [InlineKeyboardButton(text="7", callback_data="sieges_7"), InlineKeyboardButton(text="8", callback_data="sieges_8")],
        [InlineKeyboardButton(text="Назад", callback_data="sieges_Назад")]])
    return kb

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
        InlineKeyboardButton(text="Назад", callback_data=f"player_Назад")
    )

    builder.adjust(1)

    return builder.as_markup()

async def get_player_profile_actions(player_id: int) -> InlineKeyboardMarkup:
    """
    Отдает возможные действия с анкетой
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Опубликовать", callback_data=f"publish_player_{player_id}")],
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
        [InlineKeyboardButton(text="Назад", callback_data="patch_player_field_Назад")],
    ])

    return kb