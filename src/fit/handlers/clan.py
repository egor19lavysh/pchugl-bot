from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.fit.keyboards import *
from src.fit.states import *
from src.clan.keyboards import (language_kb as clan_language_kb,
                                  hydra_kb as clan_hydra_kb,
                                  himera_kb as clan_himera_kb,
                                  lkv_kb as clan_lkv_kb,
                                  sieges_kb as clan_sieges_kb)
from src.fit.handlers.handlers import start_fit


router = Router()


LANGUAGE = "Укажите язык:"
HYDRA = "Укажите гидру:"
HIMERA = "Укажите химеру:"
LKV = "Укажите ЛКВ:"
SIEGES = "Укажите осады:"
BACK = "Назад"
SKIP = "Пропустить"
SEACH_TYPE = "Выбери тип поиска:"

@router.callback_query(SeacrhFilter.clan_lang)
async def clan_lang_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.edit_text(data, reply_markup=None)

    if data == BACK:
        await callback.message.answer(SEACH_TYPE, reply_markup=await search_type())
        await state.set_state(None)
        return

    if data not in ["RU", "UA", "EN", "Другое", SKIP]:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(LANGUAGE, reply_markup=await clan_language_kb(skip=True))
        return
    
    if data == SKIP:
        data = None
    
    await state.update_data(
        language=data
    )

    await callback.message.answer(HYDRA, reply_markup=await clan_hydra_kb(skip=True))
    await state.set_state(SeacrhFilter.clan_hydra)

@router.callback_query(SeacrhFilter.clan_hydra)
async def clan_hydra_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.edit_text(data, reply_markup=None)


    if data == BACK:
        await callback.message.answer(LANGUAGE, reply_markup=await clan_language_kb(skip=True))
        await state.set_state(SeacrhFilter.clan_lang)
        return

    if data not in "До 1В, 4В, 8В, 12В, 16В, 20В, 24В, От 28В".split(", ") + [SKIP]:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(HYDRA, reply_markup=await clan_hydra_kb(skip=True))
        return
    
    if data == SKIP:
        data = None
    
    await state.update_data(
        requirements_hydra=data
    )

    await callback.message.answer(HIMERA, reply_markup=await clan_himera_kb(skip=True))
    await state.set_state(SeacrhFilter.clan_himera)

@router.callback_query(SeacrhFilter.clan_himera)
async def clan_himera_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.edit_text(data, reply_markup=None)


    if data == BACK:
        await callback.message.answer(HYDRA, reply_markup=await clan_hydra_kb(skip=True))
        await state.set_state(SeacrhFilter.clan_hydra)
        return

    if data not in "до 100К, 200К, 300К, 400К, 500К, 600К, 700К, от 800К".split(", ") + [SKIP]:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(HIMERA, reply_markup=await clan_himera_kb(skip=True))
        return
    
    if data == SKIP:
        data = None
    
    await state.update_data(
        requirements_himera=data
    )

    await callback.message.answer(LKV, reply_markup=await clan_lkv_kb(skip=True))
    await state.set_state(SeacrhFilter.clan_lkv)

@router.callback_query(SeacrhFilter.clan_lkv)
async def clan_lkv_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.edit_text(data, reply_markup=None)


    if data == BACK:
        await callback.message.answer(HIMERA, reply_markup=await clan_himera_kb(skip=True))
        await state.set_state(SeacrhFilter.clan_himera)
        return

    if data not in "До 5, 6, 7, 8".split(", ") + [SKIP]:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(LKV, reply_markup=await clan_lkv_kb(skip=True))
        return
    
    if data == SKIP:
        data = None
    
    await state.update_data(
        requirements_lkv=data
    )

    await callback.message.answer(SIEGES, reply_markup=await clan_sieges_kb(skip=True))
    await state.set_state(SeacrhFilter.clan_sieges)

@router.callback_query(SeacrhFilter.clan_sieges)
async def clan_sieges_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.edit_text(data, reply_markup=None)


    if data == BACK:
        await callback.message.answer(LKV, reply_markup=await clan_lkv_kb(skip=True))
        await state.set_state(SeacrhFilter.clan_lkv)
        return

    if data not in "До 5, 6, 7, 8".split(", ") + [SKIP]:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(SIEGES, reply_markup=await clan_sieges_kb(skip=True))
        return
    
    if data == SKIP:
        data = None
        
    await state.update_data(
        sieges_league=data
    )

    await start_fit(bot=callback.bot, user_id=callback.from_user.id, state=state)

    
