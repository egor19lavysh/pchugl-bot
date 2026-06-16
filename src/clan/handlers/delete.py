from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from src.clan.service import service
from src.clan.keyboards import get_confirm_delete
from src.clan.states import DeleteClanStates
from aiogram.fsm.context import FSMContext
from src.start.handlers import profiles_cmd
from src.clan.handlers.read import user_clans_handler



router = Router()

CONFIRM = "Вы точно хотите удалить анкету {title}?"
NO_PROFILE = "Почему-то анкета не нашлась..."
SUCCESSFUL_DELETE = "Ваша анкета {title} удалена"
DELETE_DENIED = "Удаление анкеты отменено"
INCORRECT_VALUE = "Некорректное значение!"

@router.callback_query(F.data.startswith("delete_clan_"))
async def delete_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    clan_id = int(callback.data.split("_")[-1])
    if clan := await service.get_clan_by_id(clan_id=clan_id):
        await state.update_data(
            clan_id=clan_id,
            title = clan.title
        )
        await callback.message.answer(CONFIRM.format(title=clan.title), reply_markup=await get_confirm_delete())
        await state.set_state(DeleteClanStates.confirm)
    else:
        await callback.message.answer(NO_PROFILE)

@router.callback_query(DeleteClanStates.confirm)
async def delete_confirm_handler(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]

    data = await state.get_data()

    if answer == "Да":
        if clan_id := data.get("clan_id"):
            await service.delete_clan(clan_id=clan_id)
            await callback.message.answer(SUCCESSFUL_DELETE.format(title=data.get("title", "")))
        else:
            await callback.message.answer(NO_PROFILE)
    elif answer == "Нет":
        await callback.message.answer(DELETE_DENIED)
    else:
        await callback.message.answer(INCORRECT_VALUE)
        return
    
    await state.clear()
    await user_clans_handler(callback)

