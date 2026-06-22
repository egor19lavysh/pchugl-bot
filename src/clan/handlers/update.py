from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.clan.service import service
from src.clan.states import UpdateClanStates
from src.clan.keyboards import get_clan_fields_for_update
from aiogram.fsm.context import FSMContext
from src.clan.keyboards import *
from src.clan.handlers.read import user_clans_handler, user_clans_handler_with_bot
from src.clan.models import Clan
from src.clan.handlers.create import (TITLE, TG_TAG, NICKNAME, LEVEL,
                                        PHOTO,
                                        LANGUAGE,
                                        HYDRA,
                                        HIMERA,
                                        LKV,
                                        SIEGES)



router = Router()

FIELD = "Выберите поле, которое хотите обновить:"
BACK = "Назад"
INCORRECT_VALUE = "Некорректное значение!"
LOST_CLAN_ID = "Я потерял анкету... Попробуйте снова"
ERROR = "Произошла ошибка. Попробуйте еще раз."
NEED_TEXT = "Введите текст!"
BACK = "Назад"
SUCCESS = "Изменения успешно сохранены"
FAIL = "Что-то пошло не так... Попробуйте позже"
DENY_UPDATE = "Изменение поля отменено"
NEED_PHOTO = "Отправьте картинку или нажмите пропустить!"

@router.callback_query(F.data.startswith("update_clan_"))
async def update_clan_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    clan_id = int(callback.data.split("_")[-1])
    await state.update_data(clan_id=clan_id)

    await callback.message.answer(FIELD, reply_markup=await get_clan_fields_for_update())
    await state.set_state(UpdateClanStates.choice)

@router.callback_query(UpdateClanStates.choice)
async def field_handler(callback: CallbackQuery, state: FSMContext):
    
    field = callback.data.split("_")[-1]
    
    if field == BACK:
        await state.clear()
        await user_clans_handler(callback)
        return
    
    await callback.answer()
    await callback.message.edit_text(field, reply_markup=None)

    data = await state.get_data()
    if data.get("clan_id"):

        if field == title:
            await callback.message.answer(TITLE, reply_markup=await back_kb())
            await state.set_state(UpdateClanStates.title)
        elif field == nick:
            await callback.message.answer(NICKNAME, reply_markup=await back_kb())
            await state.set_state(UpdateClanStates.nickname)
        elif field == tg:
            await callback.message.answer(TG_TAG, reply_markup=await tg_tag())
            await state.set_state(UpdateClanStates.tg_tag)
        elif field == level:
            await callback.message.answer(LEVEL, reply_markup=await level_kb())
            await state.set_state(UpdateClanStates.level)
        elif field == photo:
            await callback.message.answer(PHOTO, reply_markup=await photo_kb())
            await state.set_state(UpdateClanStates.photo)
        elif field == lang:
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            await state.set_state(UpdateClanStates.language)
        elif field == hydra:
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            await state.set_state(UpdateClanStates.requirements_hydra)
        elif field == himera:
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            await state.set_state(UpdateClanStates.requirements_himera)
        elif field == lkv:
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            await state.set_state(UpdateClanStates.requirements_lkv)
        elif field == sieges:
            await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
            await state.set_state(UpdateClanStates.sieges_league)
        else:
            await callback.message.answer(INCORRECT_VALUE)
            await callback.message.answer(FIELD, reply_markup=await get_clan_fields_for_update())
            return
    else:
        await callback.message.answer(LOST_CLAN_ID)

async def update_field(bot: Bot, user_id: int, state: FSMContext, field: str, value: int | str | None) -> Clan:
    """
    Вспомогательная функция, чтобы удобно проверять state и сохранять новые изменения. 
    После сохранение перенаправление на хендлер со всеми анкетами.
    """
    
    data = await state.get_data()
    if clan_id := data.get("clan_id"):
        if await service.update_clan(clan_id=clan_id, field_name=field, value=value):
            await bot.send_message(chat_id=user_id, text=SUCCESS, reply_markup=ReplyKeyboardRemove())
        else:
            await bot.send_message(chat_id=user_id, text=FAIL, reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(chat_id=user_id, text="Я потерял анкету... Попробуйте снова", reply_markup=ReplyKeyboardRemove())

    await state.clear()
    await user_clans_handler_with_bot(bot=bot, user_id=user_id)
         


@router.message(UpdateClanStates.title)
async def title_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_clans_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
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

@router.message(UpdateClanStates.nickname)
async def nickname_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await state.clear()
                await message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
                await user_clans_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
                return
            
            await update_field(bot=message.bot,
                               user_id=message.from_user.id,
                               state=state,
                               field="name",
                               value=message.text)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(UpdateClanStates.tg_tag)
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
                await user_clans_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
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

@router.callback_query(UpdateClanStates.level)
async def level_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_clans_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        
        if data not in "До 20, 21, 22, 23, 24, 25, 26, От 27".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LEVEL, reply_markup=await level_kb())
            return
        
        await update_field(bot=callback.bot,
                               user_id=callback.from_user.id,
                               state=state,
                               field="level",
                               value=data)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.message(UpdateClanStates.photo)
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
                await user_clans_handler_with_bot(bot=message.bot, user_id=message.from_user.id)
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


@router.callback_query(UpdateClanStates.language)
async def language_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_clans_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
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



@router.callback_query(UpdateClanStates.requirements_hydra)
async def requirements_hydra_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_clans_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        if data not in "До 1В, 4В, 8В, 12В, 16В, 20В, 24В, От 28В".split(", "):
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


@router.callback_query(UpdateClanStates.requirements_himera)
async def requirements_himera_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_clans_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        if data not in "До 100К, 200К, 300К, 400К, 500К, 600К, 700К, От 800К".split(", "):
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

@router.callback_query(UpdateClanStates.requirements_lkv)
async def requirements_lkv_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_clans_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        if data not in "До 5, 6, 7, 8".split(", "):
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

@router.callback_query(UpdateClanStates.sieges_league)
async def sieges_league_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await state.clear()
            await callback.message.answer(DENY_UPDATE, reply_markup=ReplyKeyboardRemove())
            await user_clans_handler_with_bot(bot=callback.bot, user_id=callback.from_user.id)
            return
        
        if data not in "До 5, 6, 7, 8".split(", "):
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