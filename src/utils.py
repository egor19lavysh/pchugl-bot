from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from functools import wraps
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from typing import Union


async def is_subscriber(bot: Bot, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь подписчиком канала @pcheloteka.
    """
    user = await bot.get_chat_member(chat_id="@pcheloteka", user_id=user_id)
    return user.status != "left"



def cancel_on_command(func):
    """
    Декоратор, который отменяет создание анкеты при вводе любой команды.
    Если пользователь вводит команду (начинается с '/'), состояние очищается
    и отправляется уведомление об отмене.
    """
    @wraps(func)
    async def wrapper(event: Union[Message, CallbackQuery], state: FSMContext, *args, **kwargs):
        if isinstance(event, Message):
            message = event 

            if message.text and message.text.startswith('/'):
                await state.clear()
                await message.answer("❌Создание анкеты отменено", reply_markup=ReplyKeyboardRemove())
                return
            
        return await func(event, state, *args, **kwargs)
    
    return wrapper

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