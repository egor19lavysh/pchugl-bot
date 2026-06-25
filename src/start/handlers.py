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

INFO_TEXT = """
*Информация о боте ПЧУГЛ*

*Что делают кнопки:*
• /register — создать новую анкету игрока или клана.
• /profiles — увидеть свои текущие анкеты и управлять ими.
• /fit — искать подходящих игроков или кланы по фильтрам.
• /info — прочитать эту справку.

*Процесс создания анкеты:*
1. Нажми /register.
2. Выбери игрока или клан.
3. Заполни данные по шагам: название, язык, осады и т.п.
4. В конце сохрани анкету и при необходимости опубликуй.
5. Опубликованная анкета становится доступна в поиске другим пользователям.

*Как работает поиск:*
• В /fit сначала выбери, что ищешь — игрока или клан.
• Можно искать все анкеты или задать фильтры.
• Фильтры указывают язык, гидру, химеру, ЛКВ и другие параметры.
• Система показывает случайный набор подходящих анкет на странице.

*Публикация, отзывы и обновление анкет:*
• Публикация делает анкету видимой в общем поиске.
• Отзывы помогают другим пользователям оценить качество профиля.
• За каждый профиль можно оставить отзыв и выставить рейтинг.
• Обновление анкеты позволяет изменить данные и снова сохранить ее.
"""

@router.message(Command("info"))
async def info_cmd(message: Message, state: FSMContext = None):
    if state:    
        await state.clear()
    await message.answer(INFO_TEXT)

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


