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

@router.callback_query(SeacrhFilter.player_lang)
async def player_lang_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.delete()

    if data == BACK:
        await callback.message.answer(SEACH_TYPE, reply_markup=await search_type())
        await state.set_state(None)
        return

    if data not in ["RU", "UA", "EN", "Другое", SKIP]:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(LANGUAGE, reply_markup=await player_language_kb(skip=True))
        return
    
    if data == SKIP:
        data = None
    
    await state.update_data(
        language=data
    )

    await callback.message.answer(HYDRA, reply_markup=await player_hydra_kb(skip=True))
    await state.set_state(SeacrhFilter.player_hydra)

@router.callback_query(SeacrhFilter.player_hydra)
async def player_hydra_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.delete()


    if data == BACK:
        await callback.message.answer(LANGUAGE, reply_markup=await player_language_kb(skip=True))
        await state.set_state(SeacrhFilter.player_lang)
        return
    
    elif data == SKIP:
        data = None

    else:
        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HYDRA, reply_markup=await player_hydra_kb(skip=True))
            return

        if data not in [1, 2, 4, 8, 12, 16, 20, 24]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HYDRA, reply_markup=await player_hydra_kb(skip=True))
            return
    
    
    await state.update_data(
        requirements_hydra=data
    )

    await callback.message.answer(HIMERA, reply_markup=await player_himera_kb(skip=True))
    await state.set_state(SeacrhFilter.player_himera)

@router.callback_query(SeacrhFilter.player_himera)
async def player_himera_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.delete()


    if data == BACK:
        await callback.message.answer(HYDRA, reply_markup=await player_hydra_kb(skip=True))
        await state.set_state(SeacrhFilter.player_hydra)
        return
    
    elif data == SKIP:
        data = None

    else:
        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HIMERA, reply_markup=await player_himera_kb(skip=True))
            return
            
        if data not in [1, 2, 4, 8, 12, 16, 20, 24]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HIMERA, reply_markup=await player_himera_kb(skip=True))
            return
    
    await state.update_data(
        requirements_himera=data
    )

    await callback.message.answer(LKV, reply_markup=await player_lkv_kb(skip=True))
    await state.set_state(SeacrhFilter.player_lkv)

@router.callback_query(SeacrhFilter.player_lkv)
async def player_lkv_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.delete()


    if data == BACK:
        await callback.message.answer(HIMERA, reply_markup=await player_himera_kb(skip=True))
        await state.set_state(SeacrhFilter.player_himera)
        return
    
    elif data == SKIP:
        data = None

    else:
        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LKV, reply_markup=await player_lkv_kb(skip=True))
            return
            
        if data not in [101, 100, 200, 300, 400, 500, 600, 700]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LKV, reply_markup=await player_lkv_kb(skip=True))
            return
    
    await state.update_data(
        requirements_lkv=data
    )

    await callback.message.answer(SIEGES, reply_markup=await player_sieges_kb(skip=True))
    await state.set_state(SeacrhFilter.player_sieges)

@router.callback_query(SeacrhFilter.player_sieges)
async def player_sieges_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    await callback.message.delete()


    if data == BACK:
        await callback.message.answer(LKV, reply_markup=await player_lkv_kb(skip=True))
        await state.set_state(SeacrhFilter.player_lkv)
        return
    
    elif data == SKIP:
        data = None

    else:
        try:
            data = int(data)
        except:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(SIEGES, reply_markup=await player_sieges_kb(skip=True))
            return
            
        if data not in [5, 6, 7, 8]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(SIEGES, reply_markup=await player_sieges_kb(skip=True))
            return
        
    await state.update_data(
        sieges_league=data
    )

    await start_fit(bot=callback.bot, user_id=callback.from_user.id, state=state)

    
