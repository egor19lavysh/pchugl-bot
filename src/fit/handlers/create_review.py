from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from src.fit.states import ReviewStates, FitChoice
from src.fit.keyboards import review_back, review_score_kb
from src.fit.service import service
from src.fit.handlers.list_review import format_review_text


router = Router()



@router.callback_query(F.data.startswith("review_score_"))
async def review_score_callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    score_part = callback.data.split("_")[-1]
    profile_id = callback.data.split("_")[-2]

    await callback.message.edit_text(score_part, reply_markup=None)

    try:
        score = int(score_part)
        profile_id = int(profile_id)
    except ValueError:
        await callback.message.answer("Ошибка оценки. Повторите попытку.", reply_markup=await review_score_kb(profile_id=profile_id))
        return

    if score < 1 or score > 5:
        await callback.message.answer("Оценка должна быть от 1 до 5.", reply_markup=await review_score_kb(profile_id=profile_id))
        return

    await state.update_data(score=score)
    await state.set_state(ReviewStates.text)

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text="Напишите текст отзыва:",
        reply_markup=await review_back(profile_id=profile_id)
    )


@router.callback_query(F.data.regexp(r"^review_(player|clan)_\d+$"))
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
    
    await state.update_data(profile_id=profile_id, entity=entity)

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text="Выберите оценку:",
        reply_markup=await review_score_kb(profile_id=profile_id)
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

    review = await service.create_review(entity=entity, profile_id=profile_id, reviewer=message.from_user.username, score=score, text=text)
    if review is None:
        await message.answer("Не удалось создать отзыв.", reply_markup=await review_back(profile_id=profile_id))
        return
    
    
    await service.notificate_user(bot=message.bot, profile_id=profile_id, entity=entity, msg="Вам оставили отзыв:\n" + format_review_text(review=review))

    await message.answer("Отзыв создан.", reply_markup=await review_back(profile_id=profile_id))
