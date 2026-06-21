from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from src.fit.states import ReviewStates
from src.fit.keyboards import review_control_kb
from src.fit.service import service
from src.fit.handlers.handlers import show_profile


router = Router()



@router.callback_query(F.data == "review_back")
async def back_to_profile_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await show_profile(bot=callback.bot, user_id=callback.from_user.id, state=state)


@router.callback_query(F.data.startswith("review_"))
async def create_review_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.message.answer("Ошибка данных для отзыва.")
        return

    entity = parts[1]
    try:
        profile_id = int(parts[2])
    except ValueError:
        await callback.message.answer("Неверный id профиля.")
        return

    await state.update_data(entity=entity, profile_id=profile_id)
    await state.set_state(ReviewStates.score)

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text="Укажите оценку от 1 до 5:",
        reply_markup=await review_control_kb()
    )


@router.message(ReviewStates.score)
async def review_score_handler(message: Message, state: FSMContext):
    text = message.text.strip() if message.text else ""

    try:
        score = int(text)
    except ValueError:
        await message.answer("Пожалуйста, укажите оценку числом от 1 до 5.")
        return

    if score < 1 or score > 5:
        await message.answer("Оценка должна быть в диапазоне от 1 до 5.")
        return

    await state.update_data(score=score)
    await state.set_state(ReviewStates.text)
    await message.answer(
        "Напишите текст отзыва:",
        reply_markup=await review_control_kb()
    )


@router.message(ReviewStates.text)
async def review_text_handler(message: Message, state: FSMContext):
    text = message.text.strip() if message.text else ""

    data = await state.get_data()
    entity = data.get("entity")
    profile_id = data.get("profile_id")
    score = data.get("score")

    if entity is None or profile_id is None or score is None:
        await state.clear()
        await message.answer("Ошибка состояния. Попробуйте заново.", reply_markup=ReplyKeyboardRemove())
        return

    review = await service.create_review(entity=entity, profile_id=profile_id, score=score, text=text)
    if review is None:
        await state.clear()
        await message.answer("Не удалось создать отзыв. Анкета не найдена.", reply_markup=ReplyKeyboardRemove())
        return

    await message.answer("Отзыв создан.", reply_markup=ReplyKeyboardRemove())
    await show_profile(bot=message.bot, user_id=message.from_user.id, state=state)

