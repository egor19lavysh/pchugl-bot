from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                            ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.clan.models import Clan


async def tg_tag() -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Подставить свой автоматически")],
        [KeyboardButton(text="Пропустить")],
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

async def photo_kb() -> ReplyKeyboardMarkup:
    btns = [
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

async def level_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 20", callback_data="level_До 20"), 
         InlineKeyboardButton(text="21", callback_data="level_21")],
        [InlineKeyboardButton(text="22", callback_data="level_22"), 
         InlineKeyboardButton(text="23", callback_data="level_23")],
        [InlineKeyboardButton(text="24", callback_data="level_24"), 
         InlineKeyboardButton(text="25", callback_data="level_25")],
        [InlineKeyboardButton(text="26", callback_data="level_26"), 
         InlineKeyboardButton(text="От 27", callback_data="level_От 27")],
        [InlineKeyboardButton(text="Назад", callback_data="level_Назад")],

    ])
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
        [InlineKeyboardButton(text="Нет", callback_data="lkv_0"), InlineKeyboardButton(text="До 100K", callback_data="lkv_100")],
        [InlineKeyboardButton(text="От 100K", callback_data="lkv_2"), InlineKeyboardButton(text="От 200K", callback_data="lkv_200")],
        [InlineKeyboardButton(text="От 300К", callback_data="lkv_300"), InlineKeyboardButton(text="От 400K", callback_data="lkv_400")],
        [InlineKeyboardButton(text="От 500К", callback_data="lkv_500"), InlineKeyboardButton(text="От 600K", callback_data="lkv_600")],
        [InlineKeyboardButton(text="От 700К", callback_data="lkv_700"), InlineKeyboardButton(text="Назад", callback_data="lkv_Назад")],

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

async def back_kb() -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

async def get_user_clan_profiles(clans: list[Clan]) -> InlineKeyboardMarkup:
    """
    Клавиатура, которая отдает список профилей пользователя как игрока
    """
    builder = InlineKeyboardBuilder()

    for clan in clans:
        builder.add(
            InlineKeyboardButton(text=clan.title, callback_data=f"clan_{clan.id}")
        )
    
    builder.add(
        InlineKeyboardButton(text="Опубликовать все", callback_data=f"publish_clans")
    )

    builder.add(
        InlineKeyboardButton(text="Назад", callback_data=f"clan_Назад")
    )

    builder.adjust(1)

    return builder.as_markup()

async def get_clan_profile_actions(clan_id: int, is_published: bool = False) -> InlineKeyboardMarkup:
    """
    Отдает возможные действия с анкетой
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Опубликовать", callback_data=f"publish_clan_{clan_id}") if not is_published else InlineKeyboardButton(text="Снять с публикации", callback_data=f"unpublish_clan_{clan_id}") ],
        [InlineKeyboardButton(text="Изменить", callback_data=f"update_clan_{clan_id}")],
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_clan_{clan_id}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"back_from_clan")],

    ])

    return kb

async def get_confirm_delete() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="confirm_delete_clan_Да"), InlineKeyboardButton(text="Нет", callback_data="confirm_delete_clan_Нет")]
    ])

    return kb

async def back_to_clan(clan_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"clan_{clan_id}")]
    ])
    return kb

async def back_to_clans() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"clan")]
    ])
    return kb

title = "Название анкеты"
nick = "Название клана"
tg = "Тг юзернейм"
photo = "Картинка"
level = "Уровень"
lang = "Язык"
hydra = "Гидра"
himera = "Химера"
lkv = "ЛКВ"
sieges = "Осады"
clan_tag = "Тег клана"
async def get_clan_fields_for_update() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title, callback_data="patch_clan_field_" + title)],
        [InlineKeyboardButton(text=nick, callback_data="patch_clan_field_" + nick)],
        [InlineKeyboardButton(text=tg, callback_data="patch_clan_field_" + tg)],
        [InlineKeyboardButton(text=level, callback_data="patch_clan_field_" + level)],
        [InlineKeyboardButton(text=photo, callback_data="patch_clan_field_" + photo)],
        [InlineKeyboardButton(text=lang, callback_data="patch_clan_field_" + lang)],
        [InlineKeyboardButton(text=hydra, callback_data="patch_clan_field_" + hydra)],
        [InlineKeyboardButton(text=himera, callback_data="patch_clan_field_" + himera)],
        [InlineKeyboardButton(text=lkv, callback_data="patch_clan_field_" + lkv)],
        [InlineKeyboardButton(text=sieges, callback_data="patch_clan_field_" + sieges)],
        [InlineKeyboardButton(text=clan_tag, callback_data="patch_clan_field_" + clan_tag)],
        [InlineKeyboardButton(text="Назад", callback_data="patch_clan_field_Назад")],
    ])

    return kb

async def publish_again(clan_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Опубликовать снова", callback_data=f"publish_clan_{clan_id}")]
        ]
    )

    return kb

async def final_action_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сохранить анкету", callback_data="final_1")],
        [InlineKeyboardButton(text="Сохранить и опубликовать анкету", callback_data="final_2")]
    ])