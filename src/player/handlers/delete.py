from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from src.player.service import service
from src.player.keyboards import get_confirm_delete
from src.player.states import DeletePlayerStates
from aiogram.fsm.context import FSMContext
from src.utils import cancel_on_command
from src.start.handlers import profiles_cmd
from src.player.handlers.read import user_players_handler



router = Router()

CONFIRM = "Вы точно хотите удалить анкету {title}?"
NO_PROFILE = "Почему-то анкета не нашлась..."
SUCCESSFUL_DELETE = "Ваша анкета {title} удалена"
DELETE_DENIED = "Удаление анкеты отменено"
INCORRECT_VALUE = "Некорректное значение!"

@router.callback_query(F.data.startswith("delete_player_"))
async def delete_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    player_id = int(callback.data.split("_")[-1])
    if player := await service.get_player_by_id(player_id=player_id):
        await state.update_data(
            player_id=player_id,
            title = player.title
        )
        await callback.message.answer(CONFIRM.format(title=player.title), reply_markup=await get_confirm_delete())
        await state.set_state(DeletePlayerStates.confirm)
    else:
        await callback.message.answer(NO_PROFILE)

@router.callback_query(DeletePlayerStates.confirm)
@router.message(DeletePlayerStates.confirm)
@cancel_on_command
async def delete_confirm_handler(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]

    data = await state.get_data()

    if answer == "Да":
        if player_id := data.get("player_id"):
            await service.delete_player(player_id=player_id)
            await callback.message.answer(SUCCESSFUL_DELETE.format(title=data.get("title", "")))
        else:
            await callback.message.answer(NO_PROFILE)
    elif answer == "Нет":
        await callback.message.answer(DELETE_DENIED)
    else:
        await callback.message.answer(INCORRECT_VALUE)
        return
    
    await state.clear()
    await user_players_handler(callback)

