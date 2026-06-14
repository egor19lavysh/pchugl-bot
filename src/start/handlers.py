from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from .keyboards import *

router = Router()

START_TEXT = """
🐝 *ПЧУГЛ Бот*

🎮 Регистрация: /register
👤 Мои анкеты: /profiles
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
    await message.answer("Выбери, кто ты:", reply_markup=await register_kb())

@router.message(Command("profiles"))
async def profiles_cmd(message: Message):
    await message.answer("Выбери тип анкеты:", reply_markup=await profiles_kb())