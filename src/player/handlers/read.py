from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.player.service import service
from src.player.keyboards import get_user_player_profiles, get_player_profile_actions
from src.start.handlers import profiles_cmd


router = Router()

ERROR = "Произошла ошибка. Попробуйте еще раз."
PROFILES = "Вот твои анкеты игрока:"
NO_PROFILES = "У тебя еще нет анкет. Можешь создать их командой /register"
NO_PROFILE = "Почему-то анкета не нашлась..."
BACK = "Назад"
TITLE = "***{title}***\n"

@router.callback_query(F.data == "player")
async def user_players_handler(callback: CallbackQuery):
    await callback.answer()
    # try:
    await callback.message.delete()

    if players := await service.get_player(user_id=callback.from_user.id):
         await callback.message.answer(PROFILES, reply_markup=await get_user_player_profiles(players=players))
    else:
        await callback.message.answer(NO_PROFILES)

    # except Exception as e:
    #     print(e)
    #     await callback.message.answer(ERROR)

async def user_players_handler_with_bot(bot: Bot, user_id: int):
    """
    Вспомогательная функция, чтобы перенаправлять на все анкеты
    """

    #try:

    if players := await service.get_player(user_id=user_id):
         await bot.send_message(chat_id=user_id, text=PROFILES, reply_markup=await get_user_player_profiles(players=players))
    else:
        await bot.send_message(chat_id=user_id, text=NO_PROFILES)

    # except Exception as e:
    #     print(e)
    #     await callback.message.answer(ERROR)

@router.callback_query(F.data.startswith("player_"))
async def player_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    data = callback.data.split("_")[-1]

    if data == BACK:
        await profiles_cmd(callback.message)
        return
    
    player_id = int(data)
    player_info = await service.get_player_info(player_id=player_id)
    player = await service.get_player_by_id(player_id=player_id)

    if player_info:
        await callback.message.answer(TITLE.format(title=player.title) + player_info, reply_markup=await get_player_profile_actions(player_id=player_id, is_published=player.is_published))
    else:
        await callback.message.answer(NO_PROFILE)

@router.callback_query(F.data == "back_from_profile")
async def back_from_profile(callback: CallbackQuery):
    await user_players_handler(callback)

