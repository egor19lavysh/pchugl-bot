from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.clan.service import service
from src.clan.states import ClanStates
from aiogram.fsm.context import FSMContext
from src.clan.keyboards import *


router = Router()

TITLE = "Введите название анкеты (видно только вам):"
NICKNAME = "Введите название клана:"
TG_TAG = "Введите свой тг юзернейм (без @):"
PHOTO = "Отправьте картинку клана:"
LEVEL = "Введите уровень клана (число от 1 до 100):"
LANGUAGE = "Укажите язык:"
HYDRA = "Укажите гидру:"
HIMERA = "Укажите химеру:"
LKV = "Укажите ЛКВ:"
SIEGES = "Укажите осады:"
REGISTER_LIMIT = "Достигнут лимит регистраций. Вы можете изменить или удалить старые анкеты кланов."
ERROR = "Произошла ошибка. Попробуйте еще раз."
NEED_TEXT = "Введите текст!"
NEED_PHOTO = "Отправьте картинку или нажмите пропустить!"
BACK = "Назад"
SUCCESSFUL_SAVING = "Анкета клана сохранена. Вы можете ее посмотреть, опубликовать, изменить или удалить с помощью /profiles"
SAVING_FAILED = "При сохранении ошибка. Попытайтесь позже."
DENY_PROFILE = "Создание анкеты клана отменено."

@router.callback_query(F.data == "create_clan")
async def create_clan_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    try:
        await callback.message.delete()

        answer = await service.can_register(bot=callback.bot, user_id=callback.from_user.id)
        
        if msg := answer.get("msg", False):
            await callback.message.answer(msg)

        if answer.get("can_register"):
            await state.update_data(
                user_id=callback.from_user.id
            )
            await callback.message.answer(TITLE, reply_markup=await back_kb())
            await state.set_state(ClanStates.title)
        else:
            await callback.message.answer(REGISTER_LIMIT)

    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.message(ClanStates.title)
async def title_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await message.answer(DENY_PROFILE, reply_markup=ReplyKeyboardRemove())
                await state.clear()
                return
            
            await state.update_data(
                    title=message.text
                )
            
            await message.answer(NICKNAME, reply_markup=await back_kb())
            await state.set_state(ClanStates.nickname)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)


@router.message(ClanStates.nickname)
async def nickname_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await message.answer(TITLE, reply_markup=await back_kb())
                await state.set_state(ClanStates.title)
                return
            
            await state.update_data(
                    name=message.text
                )
            
            await message.answer(TG_TAG, reply_markup=await tg_tag())
            await state.set_state(ClanStates.tg_tag)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(ClanStates.tg_tag)
async def tg_tag_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == "Подставить свой автоматически":
                tag = message.from_user.username
            elif message.text == "Пропустить":
                tag = None
            elif message.text == BACK:
                await message.answer(NICKNAME, reply_markup=await back_kb())
                await state.set_state(ClanStates.nickname)
                return
            else:
                tag = message.text
            
            await state.update_data(
                    tg_tag=tag
                )
            
            await message.answer(LEVEL, reply_markup=await level_kb())
            await state.set_state(ClanStates.level)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.callback_query(ClanStates.level)
async def level_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        level = callback.data.split("_")[-1]
        await callback.message.edit_text(text=level, reply_markup=None)

        if level == BACK:
            await callback.message.answer(TG_TAG, reply_markup=await tg_tag())
            await state.set_state(ClanStates.tg_tag)
            return

        if level not in "до 20, 21, 22, 23, 24, 25, 26, от 27".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LEVEL, reply_markup=await level_kb())
            return
        
        await state.update_data(
            level=level
        )

        await callback.message.answer(PHOTO, reply_markup=await photo_kb())
        await state.set_state(ClanStates.photo)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.message(ClanStates.photo)
async def photo_handler(message: Message, state: FSMContext):
    try:
        if message.photo:
            
            await state.update_data(
                    photo=message.photo[-1].file_id
                )

        elif message.text:

            if message.text == BACK:
                await message.answer(LEVEL, reply_markup=await level_kb())
                await state.set_state(ClanStates.level)
                return
            
            elif message.text == "Пропустить":
                await state.update_data(
                    photo=None
                )
            else:
                await message.answer(NEED_PHOTO)
                return
        else:
            await message.answer(NEED_PHOTO)
            return

        await message.answer(LANGUAGE, reply_markup=await language_kb())
        await state.set_state(ClanStates.language)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.callback_query(ClanStates.language)
async def language_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await callback.message.answer(PHOTO, reply_markup=await photo_kb())
            await state.set_state(ClanStates.photo)
            return
        
        if data not in ["RU", "UA", "EN", "Другое"]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            return
        
        await state.update_data(
            language=data
        )

        await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
        await state.set_state(ClanStates.requirements_hydra)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(ClanStates.requirements_hydra)
async def requirements_hydra_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            await state.set_state(ClanStates.language)
            return
        
        if data not in "До 1В, 4В, 8В, 12В, 16В, 20В, 24В, От 28В".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            return
        
        await state.update_data(
            requirements_hydra=data
        )

        await callback.message.answer(HIMERA, reply_markup=await himera_kb())
        await state.set_state(ClanStates.requirements_himera)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(ClanStates.requirements_himera)
async def requirements_himera_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            await state.set_state(ClanStates.requirements_hydra)
            return
        
        if data not in "до 100К, 200К, 300К, 400К, 500К, 600К, 700К, от 800К".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            return
        
        await state.update_data(
            requirements_himera=data
        )

        await callback.message.answer(LKV, reply_markup=await lkv_kb())
        await state.set_state(ClanStates.requirements_lkv)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(ClanStates.requirements_lkv)
async def requirements_lkv_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            await state.set_state(ClanStates.requirements_himera)
            return
        
        if data not in "до 5, 6, 7, 8".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            return
        
        await state.update_data(
            requirements_lkv=data
        )

        await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
        await state.set_state(ClanStates.sieges_league)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(ClanStates.sieges_league)
async def sieges_league_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            await state.set_state(ClanStates.requirements_lkv)
            return
        
        if data not in "До 5, 6, 7, 8".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
            return
        
        await state.update_data(
            sieges_league=data
        )

        await callback.message.answer("Сохраняем анкету...", reply_markup=ReplyKeyboardRemove())
        await state.set_state(None)
        await save_clan(bot=callback.bot, state=state)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

async def save_clan(bot: Bot, state: FSMContext):
    data = await state.get_data()
    try:
        await service.create_clan(**data)
        await bot.send_message(chat_id=data.get("user_id"), text=SUCCESSFUL_SAVING)
    except Exception as e:
        print(e)
        await bot.send_message(chat_id=data.get("user_id"), text=SAVING_FAILED)
    await state.clear()