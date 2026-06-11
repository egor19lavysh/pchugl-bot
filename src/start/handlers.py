from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from .keyboards import register_kb

router = Router()

START_TEXT = """
🐝 *ПЧУГЛ Бот*

🎮 Регистрация: /register
👤 Мои анкеты: /profiles  
🛡 Мои кланы: /clans
🔎 Найти тиммейта: /fit

📢 Опубликовать анкету → 1д (без подписки) / 7д (с подпиской)
⭐️ Оценивай игроков и кланы с отзывами

👇 Начинай с /register
"""

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(START_TEXT)

@router.message(Command("register"))
async def register_cmd(message: Message):
    await message.answer("Выбери, кто ты:", reply_markup=register_kb())
