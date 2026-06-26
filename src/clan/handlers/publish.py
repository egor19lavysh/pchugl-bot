from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.clan.service import service
from src.clan.keyboards import back_to_clan, back_to_clans

router = Router()

ALREADY_PUBLISHED = "Ваша анкета уже опубликована. Вы можете ее снять с публикации или дождаться, когда она автоматически снимется."
SUCCESS = "Вана анкета успешно опубликована на "
SUB_INFO = "Вы можете увеличить количество дней публикации до 7, если подпишитесь на канал @pcheloteka"
NO_PROFILE = "Почему-то анкета не нашлась..."
UNPUBLISHED = "Ваша анкета снята с публикации"
PUBLISHED_ALL = "Все ваши анкеты опубликованы"

@router.callback_query(F.data.startswith("publish_clan_"))
async def publish_handler(callback: CallbackQuery, scheduler: AsyncIOScheduler):
    await callback.answer()
    await callback.message.delete()

    clan_id = int(callback.data.split("_")[-1])

    if await service.is_published(clan_id=clan_id):
        await callback.message.answer(ALREADY_PUBLISHED, reply_markup=await back_to_clan(clan_id=clan_id))
    else:
        days = await service.publish_clan(apscheduler=scheduler, bot=callback.bot, clan_id=clan_id)

        if days:
            days_str = "7 дней" if days == 7 else "1 день"

            await callback.message.answer(SUCCESS + days_str, reply_markup=await back_to_clan(clan_id=clan_id))
            
            if days == 1:
                await callback.message.answer(SUB_INFO)
        else:
            await callback.message.answer(NO_PROFILE, reply_markup=await back_to_clan(clan_id=clan_id))

@router.callback_query(F.data.startswith("unpublish_clan_"))
async def publish_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    clan_id = int(callback.data.split("_")[-1])

    await service.unpublish_clan(clan_id=clan_id)
    await callback.message.answer(UNPUBLISHED, reply_markup=await back_to_clan(clan_id=clan_id))

@router.callback_query(F.data == "publish_clans")
async def publish_handler(callback: CallbackQuery, scheduler: AsyncIOScheduler):
    await callback.answer()
    await callback.message.delete()

    await service.publish_clans(apscheduler=scheduler, bot=callback.bot, user_id=callback.from_user.id)
    await callback.message.answer(PUBLISHED_ALL, reply_markup=await back_to_clans())
