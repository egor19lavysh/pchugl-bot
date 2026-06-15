from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from functools import wraps
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Union


async def is_subscriber(bot: Bot, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь подписчиком канала @pcheloteka.
    """
    user = await bot.get_chat_member(chat_id="@pcheloteka", user_id=user_id)
    return user.status != "left"


PLAYER_TEMPLATE = """
*Ник*: {nickname}
*Тг юзернейм*: {tg_tag}
*Уровень*: {level}
*Сила аккаунта*: {account_strength}
*Язык*: {language}
*Гидра*: {hydra}
*Химера*: {himera}
*ЛКВ*: {lkv}
*Осады*: {sieges}
"""