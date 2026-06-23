from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.player.service import service
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
PHOTO = "Добавьте фото ваших героев:"
HYDRA = "Укажите очки на Гидра КВ:"
HIMERA = "Укажите очки на Химера КВ:"
LKV = "Укажите очки на ЛКВ:"
SIEGES = "Укажите лигу в Осадах:"
REGISTER_LIMIT = "Достигнут лимит регистраций. Вы можете изменить или удалить старые анкеты."
ERROR = "Произошла ошибка. Попробуйте еще раз."
NEED_TEXT = "Введите текст!"
BACK = "Назад"
SUCCESSFUL_SAVING = "Ваша анкета сохранена. Управлять анкетой можно через /profiles"
SAVING_FAILED = "При сохранении ошибка. Попытайтесь позже."
DENY_PROFILE = "Создание анкеты отменено."
NEED_PHOTO = "Отправьте картинку или нажмите пропустить!"
FINAL_ACTION = "Выберите действие:"


@router.callback_query(F.data == "create_player")
async def create_player_handler(callback: CallbackQuery, state: FSMContext):
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
                await message.answer(DENY_PROFILE, reply_markup=ReplyKeyboardRemove())
                await state.clear()
                return
            
            await state.update_data(
                    title=message.text
                )
            
            await message.answer(NICKNAME, reply_markup=await back_kb())
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
                await message.answer(TITLE, reply_markup=await back_kb())
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
                await message.answer(NICKNAME, reply_markup=await back_kb())
                await state.set_state(PlayerStates.nickname)
                return
            else:
                tag = message.text
            
            await state.update_data(
                    tg_tag=tag
                )
            
            await message.answer(LEVEL, reply_markup=await back_kb())
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
            
            await message.answer(ACCOUNT_STREGTH, reply_markup=await back_kb())
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
                await message.answer(LEVEL, reply_markup=await back_kb())
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
        await state.clear()
        await message.answer(ERROR)

@router.callback_query(PlayerStates.language)
async def language_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        data = callback.data.split("_")[-1]
        await callback.message.edit_text(data, reply_markup=None)

        if data == BACK:
            await callback.message.answer(ACCOUNT_STREGTH, reply_markup=await back_kb())
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

        if data == BACK:
            await callback.message.answer(LANGUAGE, reply_markup=await language_kb())
            await state.set_state(PlayerStates.language)
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

        if data == BACK:
            await callback.message.answer(HYDRA, reply_markup=await hydra_kb())
            await state.set_state(PlayerStates.requirements_hydra)
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

        if data == BACK:
            await callback.message.answer(HIMERA, reply_markup=await himera_kb())
            await state.set_state(PlayerStates.requirements_himera)
            return
        
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

        if data == BACK:
            await callback.message.answer(LKV, reply_markup=await lkv_kb())
            await state.set_state(PlayerStates.requirements_lkv)
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
        
        await state.update_data(
            sieges_league=data
        )

        await callback.message.answer(PHOTO, reply_markup=await photo_kb())
        await state.set_state(PlayerStates.photo)
            
    except Exception as e:
        print(e)
        await state.clear()
        await callback.message.answer(ERROR)

@router.message(PlayerStates.photo)
async def photo_handler(message: Message, state: FSMContext):
    try:
        if message.photo:
            
            await state.update_data(
                    photo=message.photo[-1].file_id
                )

        elif message.text:

            if message.text == BACK:
                await message.answer(SIEGES, reply_markup=await sieges_kb())
                await state.set_state(PlayerStates.sieges_league)
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
        
        await message.answer(FINAL_ACTION, reply_markup=await final_action_kb())
        await state.set_state(PlayerStates.final)
            
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer(ERROR)

@router.callback_query(PlayerStates.final)
async def final_handler(callback: CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    await callback.answer()
    await callback.message.delete()

    data = callback.data.split("_")[-1]

    if data == "1":
        await save_player(bot=callback.bot, state=state)
    elif data == "2":
        player_id = await save_player(bot=callback.bot, state=state)
        if days := await service.publish_player(apscheduler=scheduler, bot=callback.bot, player_id=player_id):
            from src.player.handlers.publish import SUCCESS, SUB_INFO
            days_str = "7 дней" if days == 7 else "1 день"
            await callback.message.answer(SUCCESS + days_str, reply_markup=await back_to_player(player_id=player_id))
            
            if days == 1:
                await callback.message.answer(SUB_INFO)
    else:
        await callback.message.answer("Некорректное значение!")
        await callback.message.answer(FINAL_ACTION, reply_markup=await final_action_kb())
        return
    
    await state.clear()


async def save_player(bot: Bot, state: FSMContext) -> int | None:
    data = await state.get_data()
    try:
        player = await service.create_player(**data)
        if player:
            await bot.send_message(chat_id=data.get("user_id"), text=SUCCESSFUL_SAVING)
            return player.id
    except Exception as e:
        print(e)
        await bot.send_message(chat_id=data.get("user_id"), text=SAVING_FAILED)