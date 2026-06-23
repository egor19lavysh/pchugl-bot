from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from .keyboards import *
from aiogram.fsm.context import FSMContext
from src.admin.service import service as admin_service


router = Router()

START_TEXT = """
🐝 *ПЧУГЛ Бот*

🎮 Регистрация: /register
👤 Мои анкеты: /profiles
🔎 Поиск анкет: /fit
ℹ️ Информация: /info

📢 Опубликовать анкету → 1д (без подписки) / 7д (с подпиской)
⭐️ Оценивай игроков и кланы с отзывами

👇 Начинай с /register
"""

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext = None):
    if state:    
        await state.clear()
    await message.answer(START_TEXT)

@router.message(Command("info"))
async def info_cmd(message: Message, state: FSMContext = None):
    if state:    
        await state.clear()
    await message.answer(START_TEXT)

@router.message(Command("test"))
async def test(message: Message):
    await message.answer(str(1/0))

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
    await fit(bot=message.bot, user_id=message.from_user.id, state=state)

@router.callback_query(F.data == "fit")
async def fit_callback(callback: CallbackQuery, state: FSMContext = None):
    await callback.answer()
    await callback.message.delete()
    await fit(bot=callback.bot, user_id=callback.from_user.id, state=state)

async def fit(bot: Bot, user_id: int, state: FSMContext = None):
    if state:
        await state.clear()
    await bot.send_message(chat_id=user_id, text="Выбери тип анкет:", reply_markup=await fit_profiles_kb())


@router.message(Command("export_profiles"))
async def export_profiles(message: Message):
    if message.from_user.id in [351124844, 1100774140]:
        await admin_service.export_profiles_excel(bot=message.bot, user_id=message.from_user.id)


