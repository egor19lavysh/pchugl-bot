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


router = Router()


LANGUAGE = "Укажите язык:"
HYDRA = "Укажите гидру:"
HIMERA = "Укажите химеру:"
LKV = "Укажите ЛКВ:"
SIEGES = "Укажите осады:"


@router.callback_query(SeacrhFilter.player_lang)
async def player_lang_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    if data not in ["RU", "UA", "EN", "Другое"]:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(LANGUAGE, reply_markup=await player_language_kb())
        return
    
    await state.update_data(
        language=data
    )

    await callback.message.answer(HYDRA, reply_markup=await player_hydra_kb())
    await state.set_state(SeacrhFilter.player_hydra)

@router.callback_query(SeacrhFilter.player_hydra)
async def player_hydra_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    if data not in "До 1В, 4В, 8В, 12В, 16В, 20В, 24В, От 28В".split(", "):
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(HYDRA, reply_markup=await player_hydra_kb())
        return
    
    await state.update_data(
        requirements_hydra=data
    )

    await callback.message.answer(HYDRA, reply_markup=await player_himera_kb())
    await state.set_state(SeacrhFilter.player_himera)

@router.callback_query(SeacrhFilter.player_himera)
async def player_himera_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    if data not in "До 1В, 4В, 8В, 12В, 16В, 20В, 24В, От 28В".split(", "):
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(HIMERA, reply_markup=await player_himera_kb())
        return
    
    await state.update_data(
        requirements_himera=data
    )

    await callback.message.answer(LKV, reply_markup=await player_lkv_kb())
    await state.set_state(SeacrhFilter.player_lkv)

@router.callback_query(SeacrhFilter.player_lkv)
async def player_lkv_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    if data not in "До 100К, 200К, 300К, 400К, 500К, 600К, 700К, От 800К".split(", "):
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(LKV, reply_markup=await player_lkv_kb())
        return
    
    await state.update_data(
        requirements_lkv=data
    )

    await callback.message.answer(SIEGES, reply_markup=await player_sieges_kb())
    await state.set_state(SeacrhFilter.player_sieges)

@router.callback_query(SeacrhFilter.player_sieges)
async def player_sieges_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split("_")[-1]

    if data not in "До 5, 6, 7, 8".split(", "):
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(SIEGES, reply_markup=await player_sieges_kb())
        return
        
    await state.update_data(
        sieges_league=data
    )

    
