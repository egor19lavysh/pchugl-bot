from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
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
import random


router = Router()

SEACH_TYPE = "Выбери тип поиска:"
LANGUAGE = "Укажите язык:"
FINISH_FIT = "Анкеты закончились!"
NO_PLAYERS = "По вашему запросу игроков не найдено"
NO_CLANS = "По вашему запросу кланов не найдено"
BACK = "Назад"
NEXT = "Дальше"
QUIT = "Выйти"




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
                await callback.message.answer(LANGUAGE, reply_markup=await player_language_kb(skip=True))
                await state.set_state(SeacrhFilter.player_lang)
            elif entity == "clan":
                await callback.message.answer(LANGUAGE, reply_markup=await clan_language_kb(skip=True))
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

    await state.set_state(None)


    if entity:
        if entity == "player":
            profiles = await service.filter_players(user_id=user_id, filters=filters)
        elif entity == "clan":
            profiles = await service.filter_clans(user_id=user_id, filters=filters)
            
        if not profiles:
            if entity == "player":
                await bot.send_message(chat_id=user_id, text=NO_PLAYERS, reply_markup=await back_to_search())
            elif entity == "clan":
                await bot.send_message(chat_id=user_id, text=NO_CLANS, reply_markup=await back_to_search())
            await state.clear()
            return
        

        random.shuffle(profiles)
        await state.update_data(
            profiles=profiles,
            page=0
        )

        await show_profiles_page(bot=bot, user_id=user_id, state=state)
    else:
        await bot.send_message(chat_id=user_id, text="Я потерял сущность поиска... Попоробуйте снова")

@router.callback_query(F.data == "fit_list")
async def fit_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await show_profiles_page(bot=callback.bot, user_id=callback.from_user.id, state=state)

async def show_profiles_page(bot: Bot, user_id: int, state: FSMContext):
    data = await state.get_data()

    profiles = data.get("profiles")
    entity = data.get("entity")
    page = data.get("page", 0)

    if profiles:
        await bot.send_message(chat_id=user_id, text="Выберите анкету:", reply_markup=await profiles_page_kb(profiles=profiles, page=page))
    else:
        if entity == "player":
            await bot.send_message(chat_id=user_id, text=NO_PLAYERS, reply_markup=await back_to_search())
        elif entity == "clan":
            await bot.send_message(chat_id=user_id, text=NO_CLANS, reply_markup=await back_to_search())
        else:
            await bot.send_message(chat_id=user_id, text="Анкеты не найдены...", reply_markup=await back_to_search())
        await state.clear()



@router.callback_query(F.data.startswith("fit_prev_") | F.data.startswith("fit_next_"))
async def fit_page_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    profiles = data.get("profiles", [])

    if not profiles:
        await callback.message.answer("Анкеты не найдены...", reply_markup=await back_to_search())
        await state.clear()
        return

    new_page = int(callback.data.split("_")[-1])

    per_page = 16
    max_page = (len(profiles) - 1) // per_page
    if new_page < 0 or new_page > max_page:
        await callback.answer("Страница недоступна", show_alert=True)
        return

    await state.update_data(page=new_page)

    kb = await profiles_page_kb(profiles=profiles, page=new_page)
    try:
        await callback.message.edit_text("Выберите анкету:", reply_markup=kb)
    except Exception:
        await callback.message.answer("Выберите анкету:", reply_markup=kb)


@router.callback_query(F.data.startswith("fit_profile_"))
async def fit_profile_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    profile_id = int(callback.data.split("_")[-1])

    data = await state.get_data()

    profiles = data.get("profiles")
    entity = data.get("entity")

    if not profiles:
        await callback.message.answer(text="Анкеты не нашлись... Попробуйте снова", reply_markup=await back_to_search())
        await state.clear()
        return

    profile = await service.get_profile(entity=entity, profile_id=profile_id)
    info = await service.get_info(profile=profile)

    
    if getattr(profile, "photo", None):
        try:
            await callback.message.answer_photo(photo=profile.photo, caption=info, reply_markup=await profile_action(entity=entity, profile_id=profile.id))
        except Exception as e:
            print(e)
            await callback.message.answer(text=info, reply_markup=await profile_action(entity=entity, profile_id=profile.id))
    else:
        await callback.message.answer(text=info, reply_markup=await profile_action(entity=entity, profile_id=profile.id))
        


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