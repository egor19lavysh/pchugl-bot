from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.player.service import service
from src.player.states import PlayerStates
from aiogram.fsm.context import FSMContext
from src.player.keyboards import *


router = Router()

TITLE = "Введите название анкеты (видно только вам):"
NICKNAME = "Введите свой никнейм:"
TG_TAG = "Введите свой тг юзернейм (без @):"
LEVEL = "Введите свой уровень (число от 1 до 100):"
ACCOUNT_STREGTH = "Введите свою силу аккаунта (число от 1 до 100):"
LANGUAGE = "Укажите язык:"
HYDRA = "Укажите гидру:"
HIMERA = "Укажите химеру:"
LKV = "Укажите ЛКВ:"
SIEGES = "Укажите осады:"
REGISTER_LIMIT = "Достигнут лимит регистраций. Вы можете изменить или удалить старые анкеты."
ERROR = "Произошла ошибка. Попробуйте еще раз."
NEED_TEXT = "Введите текст!"
BACK = "Назад"
BACK_INLINE = "Назад"
SUCCESSFUL_SAVING = "Ваша анкета сохранена. Вы можете ее посмотреть, опубликовать, изменить или удалить с помощью /profiles"
SAVING_FAILED = "При сохранении ошибка. Попытайтесь позже."
DENY_PROFILE = "Создание анкеты отменено."

@router.callback_query(F.data == "player")
async def player_handler(callback: CallbackQuery, state: FSMContext):
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
            await callback.message.answer(TITLE)
            await state.set_state(PlayerStates.title)
        else:
            await callback.message.answer(REGISTER_LIMIT)

    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.message(PlayerStates.title)
async def title_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await message.answer(DENY_PROFILE)
                await state.clear()
                return
            
            await state.update_data(
                    title=message.text
                )
            
            await message.answer(NICKNAME)
            await state.set_state(PlayerStates.nickname)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

            
@router.message(PlayerStates.nickname)
async def nickname_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await message.answer(TITLE)
                await state.set_state(PlayerStates.title)
                return
            
            await state.update_data(
                    nickname=message.text
                )
            
            await message.answer(TG_TAG, reply_markup=await tg_tag())
            await state.set_state(PlayerStates.tg_tag)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(PlayerStates.tg_tag)
async def tg_tag_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == "Подставить свой автоматически":
                tag = message.from_user.username
            elif message.text == "Пропустить":
                tag = None
            elif message.text == BACK:
                await message.answer(NICKNAME)
                await state.set_state(PlayerStates.nickname)
                return
            else:
                tag = message.text
            
            await state.update_data(
                    tg_tag=tag
                )
            
            await message.answer(LEVEL, reply_markup=ReplyKeyboardRemove())
            await state.set_state(PlayerStates.level)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(PlayerStates.level)
async def level_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await message.answer(TG_TAG, reply_markup=await tg_tag())
                await state.set_state(PlayerStates.tg_tag)
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

            await state.update_data(
                    level=num
                )
            
            await message.answer(ACCOUNT_STREGTH, reply_markup=ReplyKeyboardRemove())
            await state.set_state(PlayerStates.account_strength)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.message(PlayerStates.account_strength)
async def account_strength_handler(message: Message, state: FSMContext):
    try:
        if message.text:
            
            if message.text == BACK:
                await message.answer(LEVEL, reply_markup=ReplyKeyboardRemove())
                await state.set_state(PlayerStates.level)
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

            await state.update_data(
                    account_strength=num
                )
            
            await message.answer(LANGUAGE, reply_markup=await language_kb())
            await state.set_state(PlayerStates.language)
        else:
            await message.answer(NEED_TEXT)
            
    except Exception as e:
        print(e)
        print(await state.get_data())
        await state.clear()
        await message.answer(ERROR)

@router.callback_query(PlayerStates.language)
async def language_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK_INLINE:
            await callback.message.answer(ACCOUNT_STREGTH, reply_markup=ReplyKeyboardRemove())
            await state.set_state(PlayerStates.account_strength)
            return
        
        if data not in ["RU", "UA", "EN", "Другое"]:
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            return
        
        await state.update_data(
            language=data
        )

        await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
        await state.set_state(PlayerStates.requirements_hydra)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(PlayerStates.requirements_hydra)
async def requirements_hydra_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK_INLINE:
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            await state.set_state(PlayerStates.language)
            return
        
        if data not in "До 1В, 4В, 8В, 12В, 16В, 20В, 24В, От 28В".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            return
        
        await state.update_data(
            requirements_hydra=data
        )

        await callback.message.answer(HIMERA, reply_markup=await himera_kb())
        await state.set_state(PlayerStates.requirements_himera)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(PlayerStates.requirements_himera)
async def requirements_himera_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK_INLINE:
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            await state.set_state(PlayerStates.requirements_hydra)
            return
        
        if data not in "До 1В, 4В, 8В, 12В, 16В, 20В, 24В, От 28В".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            return
        
        await state.update_data(
            requirements_himera=data
        )

        await callback.message.answer(LKV, reply_markup=await lkv_kb())
        await state.set_state(PlayerStates.requirements_lkv)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(PlayerStates.requirements_lkv)
async def requirements_lkv_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK_INLINE:
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            await state.set_state(PlayerStates.requirements_himera)
            return
        
        if data not in "До 100К, 200К, 300К, 400К, 500К, 600К, 700К, От 800К".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            return
        
        await state.update_data(
            requirements_lkv=data
        )

        await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
        await state.set_state(PlayerStates.sieges_league)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.callback_query(PlayerStates.sieges_league)
async def sieges_league_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK_INLINE:
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            await state.set_state(PlayerStates.requirements_lkv)
            return
        
        if data not in "До 5, 6, 7, 8".split(", "):
            await callback.message.answer("Некорректное значение!")
            await callback.message.answer(SIEGES, reply_markup=await sieges_kb())
            return
        
        await state.update_data(
            sieges_league=data
        )

        await callback.message.answer("Сохраняем анкету...")
        await state.set_state(None)
        await save_player(bot=callback.bot, state=state)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

async def save_player(bot: Bot, state: FSMContext):
    data = await state.get_data()
    try:
        await service.create_player(**data)
        await bot.send_message(chat_id=data.get("user_id"), text=SUCCESSFUL_SAVING)
    except Exception as e:
        print(e)
        await bot.send_message(chat_id=data.get("user_id"), text=SAVING_FAILED)
    await state.clear()