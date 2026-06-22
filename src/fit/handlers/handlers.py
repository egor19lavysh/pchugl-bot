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
import random


router = Router()

SEACH_TYPE = "Выбери тип поиска:"
LANGUAGE = "Укажите язык:"
FINISH_FIT = "Анкеты закончились!"
BACK = "Назад"
NEXT = "Дальше"
QUIT = "Выйти"


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

    if entity:
        if entity == "player":
            profiles = await service.filter_players(user_id=user_id, filters=filters)
        elif entity == "clan":
            profiles = await service.filter_clans(user_id=user_id, filters=filters)
            
        if not profiles:
            await bot.send_message(chat_id=user_id, text="Анкеты не нашлись...", reply_markup=await back_to_search())
            await state.clear()
            return

        random.shuffle(profiles)
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
    entity = data.get("entity")

    if not profiles:
        await bot.send_message(chat_id=user_id, text="Анкеты не нашлись... Попробуйте снова", reply_markup=await back_to_search())
        await state.clear()
        return

    if -1 < index < len(profiles):
        profile = profiles[index]
        info = await service.get_info(profile=profile)
        if getattr(profile, "photo", None):
            try:
                msg = await bot.send_photo(chat_id=user_id, photo=profile.photo, caption=info, reply_markup=await profile_action(entity=entity, profile_id=profile.id))
            except Exception as e:
                print(e)
                msg = await bot.send_message(chat_id=user_id, text=info, reply_markup=await profile_action(entity=entity, profile_id=profile.id))
        else:
            msg = await bot.send_message(chat_id=user_id, text=info, reply_markup=await profile_action(entity=entity, profile_id=profile.id))

        action_msg = await bot.send_message(chat_id=user_id, text="Выберите дейстивие:", reply_markup=await fit_action())
        await state.update_data(
            profile_msg=msg.message_id,
            action_msg=action_msg.message_id
        )
        
        await state.set_state(FitChoice.choice)
    else:
        await bot.send_message(chat_id=user_id, text=FINISH_FIT, reply_markup=await back_to_search())

@router.message(FitChoice.choice)
async def fit_choice_handler(message: Message, state: FSMContext):

    data = await state.get_data()
    index = data.get("index", 0)

    if choice := message.text:

        if profile_msg := data.get("profile_msg"):
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=profile_msg)
            await state.update_data(profile_msg=None)
            
        if action_msg := data.get("action_msg"):
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=action_msg)
            await state.update_data(action_msg=None)

        if choice == NEXT:
            await state.update_data(index=index + 1)
            await show_profile(bot=message.bot, user_id=message.from_user.id, state=state)

        elif choice == BACK:
            await state.update_data(index=index - 1 if index > 0 else 0)
            await show_profile(bot=message.bot, user_id=message.from_user.id, state=state)


        elif choice == QUIT:
            await message.answer("Подбор анкет отменен", reply_markup=ReplyKeyboardRemove())
            await state.clear()

        else:
            await message.answer("Выберите одно из трех действий:", reply_markup=await fit_action())
            return


            
        
