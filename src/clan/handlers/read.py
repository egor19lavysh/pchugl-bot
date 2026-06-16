from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from src.clan.service import service
from src.clan.keyboards import get_user_clan_profiles, get_clan_profile_actions
from src.start.handlers import profiles_cmd


router = Router()

ERROR = "Произошла ошибка. Попробуйте еще раз."
PROFILES = "Вот твои анкеты кланов:"
NO_PROFILES = "У тебя еще нет анкет. Можешь создать их командой /register"
NO_PROFILE = "Почему-то анкета не нашлась..."
BACK = "Назад"
TITLE = "***{title}***\n"

@router.callback_query(F.data == "clan")
async def user_clans_handler(callback: CallbackQuery):
    await callback.answer()
    # try:
    await callback.message.delete()

    if clans := await service.get_clan(user_id=callback.from_user.id):
         await callback.message.answer(PROFILES, reply_markup=await get_user_clan_profiles(clans=clans))
    else:
        await callback.message.answer(NO_PROFILES)

    # except Exception as e:
    #     print(e)
    #     await callback.message.answer(ERROR)

async def user_clans_handler_with_bot(bot: Bot, user_id: int):
    """
    Вспомогательная функция, чтобы перенаправлять на все анкеты
    """

    #try:

    if clans := await service.get_clan(user_id=user_id):
         await bot.send_message(chat_id=user_id, text=PROFILES, reply_markup=await get_user_clan_profiles(clans=clans))
    else:
        await bot.send_message(chat_id=user_id, text=NO_PROFILES)

    # except Exception as e:
    #     print(e)
    #     await callback.message.answer(ERROR)

@router.callback_query(F.data.startswith("clan_"))
async def clan_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    data = callback.data.split("_")[-1]

    if data == BACK:
        await profiles_cmd(callback.message)
        return
    
    clan_id = int(data)
    clan_info = await service.get_clan_info(clan_id=clan_id)
    clan = await service.get_clan_by_id(clan_id=clan_id)

    if clan_info:
        if clan.photo:
            try:
                await callback.message.answer_photo(photo=clan.photo,
                                                caption=TITLE.format(title=clan.title) + clan_info, 
                                                reply_markup=await get_clan_profile_actions(clan_id=clan_id, is_published=clan.is_published))
            except Exception as e:
                print(e)
                callback.message.answer(TITLE.format(title=clan.title) + clan_info, 
                                                reply_markup=await get_clan_profile_actions(clan_id=clan_id, is_published=clan.is_published))

        else:
            await callback.message.answer(TITLE.format(title=clan.title) + clan_info, 
                                                reply_markup=await get_clan_profile_actions(clan_id=clan_id, is_published=clan.is_published))
    else:
        await callback.message.answer(NO_PROFILE)

@router.callback_query(F.data == "back_from_clan")
async def back_from_profile(callback: CallbackQuery):
    await user_clans_handler(callback)

