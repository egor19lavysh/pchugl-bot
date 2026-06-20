from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from .keyboards import *
from aiogram.fsm.context import FSMContext

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
async def start_command(message: Message, state: FSMContext = None):
    if state:    
        await state.clear()
    await message.answer(START_TEXT)

@router.message(Command("register"))
async def register_cmd(message: Message, state: FSMContext = None):
    if state:
        await state.clear()
    await message.answer("Выбери, кто ты:", reply_markup=await register_kb())

@router.message(Command("profiles"))
async def profiles_cmd(message: Message, state: FSMContext = None):
    if state:
        await state.clear()
    await message.answer("Выбери тип анкеты:", reply_markup=await profiles_kb())

@router.message(Command("fit"))
async def fit_cmd(message: Message, state: FSMContext = None):
    if state:
        await state.clear()
    await message.answer("Выбери тип анкет:", reply_markup=await fit_profiles_kb())