from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.fit.keyboards import *
from src.fit.states import *
from src.player.keyboards import (language_kb as player_language_kb,
                                  hydra_kb as player_hydra_kb,
                                  himera_kb as player_himera_kb,
                                  lkv_kb as player_lkv_kb,
                                  sieges_kb as player_sieges_kb)
from src.clan.keyboards import language_kb as clan_language_kb
from src.start.handlers import fit_cmd
from src.fit.service import service


router = Router()

SEACH_TYPE = "Выбери тип поиска:"
LANGUAGE = "Укажите язык:"
FINISH_FIT = "Анкеты закончились!"


@router.callback_query(F.data.startswith("fit_"))
async def fit_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    entity = callback.data.split("_")[-1]
    if entity in ["player", "clan"]:
        await state.update_data(
            entity=entity
            ) 

        await callback.message.answer(SEACH_TYPE, reply_markup=await search_type())

@router.callback_query(F.data.startswith("search_"))
async def search_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    data = await state.get_data()

    entity = data.get("entity")

    if entity:

        search = callback.data.split("_")[-1]
        if search == "all":
            await start_fit(bot=callback.bot, user_id=callback.from_user.id, state=state)
        elif search == "filter":
            if entity == "player":
                await callback.message.answer(LANGUAGE, reply_markup=await player_language_kb())
                await state.set_state(SeacrhFilter.player_lang)
            elif entity == "clan":
                await callback.message.answer(LANGUAGE, reply_markup=await clan_language_kb())
                await state.set_state(SeacrhFilter.clan_lang)

    else:
        await callback.message.answer("Я потерял сущность поиска... Попоробуйте снова")
        await fit_cmd(callback.message, state)


async def start_fit(bot: Bot, user_id: int, state: FSMContext):
    data = await state.get_data()
    entity = data.get("entity")
    language = data.get("language")
    sieges_league = data.get("sieges_league")
    requirements_hydra = data.get("requirements_hydra")
    requirements_himera = data.get("requirements_himera")
    requirements_lkv = data.get("requirements_lkv")

    filters = {
        "language": language,
        "sieges_league": sieges_league,
        "requirements_hydra": requirements_hydra,
        "requirements_himera": requirements_himera,
        "requirements_lkv": requirements_lkv
    }

    if entity:
        if entity == "player":
            profiles = await service.filter_players(user_id=user_id, filters=filters)
        elif entity == "clan":
            profiles = await service.filter_clans(user_id=user_id, filters=filters)
            

        await state.update_data(
            profiles=profiles,
            index=0
        )

        await show_profile(bot=bot, user_id=user_id, state=state)
    else:
        await bot.send_message(chat_id=user_id, text="Я потерял сущность поиска... Попоробуйте снова")

async def show_profile(bot: Bot, user_id: int, state: FSMContext):
    data = await state.get_data()

    profiles = data.get("profiles")
    index = data.get("index", 0)

    if not profiles:
        await bot.send_message(chat_id=user_id, text="Я потерял анкеты... Попробуйте снова")
        await state.clear()
        return

    if index < len(profiles):
        profile = profiles[index]
        info = await service.get_info(profile=profile)
        if getattr(profile, "photo", None):
            try:
                await bot.send_photo(chat_id=user_id, photo=profile.photo, caption=info)
            except Exception as e:
                print(e)
                await bot.send_message(chat_id=user_id, text=info)
        else:
            await bot.send_message(chat_id=user_id, text=info)
        await state.set_state(FitChoice.choice)
    else:
        await bot.send_message(chat_id=user_id, text=FINISH_FIT)



            
        
