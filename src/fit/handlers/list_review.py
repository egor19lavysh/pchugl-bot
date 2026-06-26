from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from src.fit.service import service
from src.fit.keyboards import review_pagination_kb, review_back
#from src.fit.handlers.handlers import show_profile
from src.fit.models import Review


router = Router()


def format_review_text(review: Review) -> str:
    return (
        f'Игрок: {"@" + review.reviewer if review.reviewer else "не указан"}\n'
        f"Оценка: {review.score}⭐️\n"
        f"Текст: {review.text}\n"
        f"Дата: {review.created_at.strftime('%Y-%m-%d %H:%M')}"
    )


@router.callback_query(F.data.startswith("reviews_prev_") | F.data.startswith("reviews_next_"))
async def reviews_navigation_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    parts = callback.data.split("_")
    if len(parts) != 5:
        await callback.message.answer("Ошибка навигации по отзывам.")
        return

    _, _, entity, profile_id_str, index_str = parts

    try:
        profile_id = int(profile_id_str)
        index = int(index_str)
    except ValueError:
        await callback.message.answer("Неверные параметры навигации.")
        return

    reviews = await service.get_reviews(entity=entity, profile_id=profile_id)
    if not reviews:
        await callback.message.answer("Пока нет отзывов для этой анкеты.", reply_markup=await review_back(profile_id=profile_id))
        return

    if index < 0 or index >= len(reviews):
        await callback.message.answer("Вы вышли за границы списка отзывов.")
        return

    await state.update_data(review_index=index)
    await callback.message.answer(
        format_review_text(reviews[index]),
        reply_markup=await review_pagination_kb(entity=entity, profile_id=profile_id, index=index, total=len(reviews))
    )


@router.callback_query(F.data.startswith("reviews_"))
async def reviews_start_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    data = await state.get_data()
    await state.set_state(None)


    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.message.answer("Ошибка данных для просмотра отзывов.")
        return

    entity = parts[1]
    try:
        profile_id = int(parts[2])
    except ValueError:
        await callback.message.answer("Неверный id профиля.")
        return

    reviews = await service.get_reviews(entity=entity, profile_id=profile_id)
    if not reviews:
        await callback.message.answer("Пока нет отзывов для этой анкеты.", reply_markup=await review_back(profile_id=profile_id))
        return

    await state.update_data(entity=entity, profile_id=profile_id, review_index=0)
    await callback.message.answer(
        format_review_text(reviews[0]),
        reply_markup=await review_pagination_kb(entity=entity, profile_id=profile_id, index=0, total=len(reviews))
    )
