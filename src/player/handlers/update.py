from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.player.service import service
from src.player.states import UpdatePlayerStates
from src.player.keyboards import get_player_fields_for_update
from aiogram.fsm.context import FSMContext
from src.player.keyboards import *
from src.player.handlers.read import user_players_handler, user_players_handler_with_bot
from src.player.models import Player
from src.player.handlers.create import (TITLE, TG_TAG, NICKNAME, LEVEL,
                                        ACCOUNT_STREGTH,
                                        LANGUAGE,
                                        HYDRA,
                                        HIMERA,
                                        LKV,
                                        SIEGES,
                                        PHOTO)



router = Router()

FIELD = "Выберите поле, которое хотите обновить:"
BACK = "Назад"
INCORRECT_VALUE = "Некорректное значение!"
LOST_PLAYER_ID = "Я потерял анкету... Попробуйте снова"
ERROR = "Произошла ошибка. Попробуйте еще раз."
NEED_TEXT = "Введите текст!"
BACK = "Назад"
SUCCESS = "Изменения успешно сохранены"
FAIL = "Что-то пошло не так... Попробуйте позже"
DENY_UPDATE = "Изменение поля отменено"
NEED_PHOTO = "Отправьте картинку или нажмите пропустить!"

@router.callback_query(F.data.startswith("update_player_"))
async def update_player_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    player_id = int(callback.data.split("_")[-1])
    await state.update_data(player_id=player_id)

    await callback.message.answer(FIELD, reply_markup=await get_player_fields_for_update())
    await state.set_state(UpdatePlayerStates.choice)

@router.callback_query(UpdatePlayerStates.choice)
async def field_handler(callback: CallbackQuery, state: FSMContext):
    
    field = callback.data.split("_")[-1]
    
    if field == BACK:
        await state.clear()
        await user_players_handler(callback)
        return
    
    await callback.answer()
    await callback.message.edit_text(field, reply_markup=None)

    data = await state.get_data()
    if data.get("player_id"):

        if field == title:
            await callback.message.answer(TITLE, reply_markup=await back_kb())
            await state.set_state(UpdatePlayerStates.title)
        elif field == nick:
            await callback.message.answer(NICKNAME, reply_markup=await back_kb())
            await state.set_state(UpdatePlayerStates.nickname)
        elif field == tg:
            await callback.message.answer(TG_TAG, reply_markup=await tg_tag())
            await state.set_state(UpdatePlayerStates.tg_tag)
        elif field == level:
            await callback.message.answer(LEVEL, reply_markup=await back_kb())
            await state.set_state(UpdatePlayerStates.level)
        elif field == account_strength:
            await callback.message.answer(ACCOUNT_STREGTH, reply_markup=await back_kb())
            await state.set_state(UpdatePlayerStates.account_strength)
        elif field == lang:
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            await state.set_state(UpdatePlayerStates.language)
        elif field == hydra:
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            await state.set_state(UpdatePlayerStates.requirements_hydra)
        elif field == himera:
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            await state.set_state(UpdatePlayerStates.requirements_himera)
        elif field == lkv:
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            await state.set_state(UpdatePlayerStates.requirements_lkv)
        elif field == sieges:
            await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
            await state.set_state(UpdatePlayerStates.sieges_league)
        elif field == photo:
            await callback.message.answer(PHOTO, reply_markup=await photo_kb())
            await state.set_state(UpdatePlayerStates.photo)
        else:
            await callback.message.answer(INCORRECT_VALUE)
            await callback.message.answer(FIELD, reply_markup=await get_player_fields_for_update())
            return
    else:
        await callback.message.answer(LOST_PLAYER_ID)

async def update_field(bot: Bot, user_id: int, state: FSMContext, field: str, value: int | str | None) -> Player:
    """
    Вспомогательная функция, чтобы удобно проверять state и сохранять новые изменения. 
    После сохранение перенаправление на хендлер со всеми анкетами.
    """
    
    data = await state.get_data()
    if player_id := data.get("player_id"):
        if await service.update_player(player_id=player_id, field_name=field, value=value):
            await bot.send_message(chat_id=user_id, text=SUCCESS, reply_markup=ReplyKeyboardRemove())
        else:
            await bot.send_message(chat_id=user_id, text=FAIL, reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(chat_id=user_id, text="Я потерял анкету... Попробуйте снова", reply_markup=ReplyKeyboardRemove())

    await state.clear()
    await user_players_handler_with_bot(bot=bot, user_id=user_id)
         


@router.message(UpdatePlayerStates.title)
async def title_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_players_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
                return
            
            await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="title",
                               value=message.text)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(UpdatePlayerStates.nickname)
async def nickname_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_players_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
                return
            
            await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="nickname",
                               value=message.text)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(UpdatePlayerStates.tg_tag)
async def tg_tag_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == "Подставить свой автоматически":
                tag = message.from_user.username
            elif message.text == "Пропустить":
                tag = None
            elif message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_players_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
                return
            else:
                tag = message.text
            
            await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="tg_tag",
                               value=tag)
            
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(UpdatePlayerStates.level)
async def level_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_players_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
                return
            
            try:
                num = int(message.text)
            except:
                await message.answer("Введите число!")
                return
            
            if not (1 <= num <= 100):
                await message.answer("Некорректное значение!")
                await message.answer(LEVEL)
                return

            await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="level",
                               value=num)
            
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(UpdatePlayerStates.account_strength)
async def account_strength_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_players_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
                return
            
            try:
                num = int(message.text)
            except:
                await message.answer("Введите число!")
                return
            
            if not (1 <= num <= 100):
                await message.answer("Некорректное значение!")
                await message.answer(ACCOUNT_STREGTH)
                return

            await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="account_strength",
                               value=num)
            
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)


@router.callback_query(UpdatePlayerStates.language)
async def language_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_players_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        if data not in ["RU", "UA", "EN", "Другое"]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            return
        
        await update_field(bot=callback.bot,
                               user_id=callback.from_user.id,
                               state=state,
                               field="language",
                               value=data)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)



@router.callback_query(UpdatePlayerStates.requirements_hydra)
async def requirements_hydra_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_players_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            return

        if data not in [1, 4, 8, 12, 16, 20, 24, 28]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            return
        
        await update_field(bot=callback.bot,
                               user_id=callback.from_user.id,
                               state=state,
                               field="requirements_hydra",
                               value=data)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)


@router.callback_query(UpdatePlayerStates.requirements_himera)
async def requirements_himera_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_players_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            return
        
        if data not in [1, 4, 8, 12, 16, 20, 24, 28]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            return
        
        await update_field(bot=callback.bot,
                               user_id=callback.from_user.id,
                               state=state,
                               field="requirements_himera",
                               value=data)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(UpdatePlayerStates.requirements_lkv)
async def requirements_lkv_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            return
        
        if data not in [100, 200, 300, 400, 500, 600, 700, 800]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            return
        
        await update_field(bot=callback.bot,
                               user_id=callback.from_user.id,
                               state=state,
                               field="requirements_lkv",
                               value=data)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(UpdatePlayerStates.sieges_league)
async def sieges_league_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_players_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
            return
        
        if data not in [5, 6, 7, 8]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
            return
        
        await update_field(bot=callback.bot,
                               user_id=callback.from_user.id,
                               state=state,
                               field="sieges_league",
                               value=data)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.message(UpdatePlayerStates.photo)
async def photo_handler(message: Message, state: FSMContext):
    try:
        if message.photo:
            
            await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="photo",
                               value=message.photo[-1].file_id)

        elif message.text:

            if message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_players_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
                return
            
            elif message.text == "Пропустить":
                await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="photo",
                               value=None)
            else:
                await message.answer(NEED_PHOTO)
                return
        else:
            await message.answer(NEED_PHOTO)
            return
        
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)