import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from src.config import settings
from src.start.handlers import router as start_router
from src.player.handlers import routers as player_routers
from src.fit.handlers import routers as fit_routers
from src.clan.handlers import routers as clan_routers
from src.player.service import service as player_service
from src.clan.service import service as clan_service
from aiogram.types.error_event import ErrorEvent
from aiogram.fsm.context import FSMContext


logger = logging.getLogger(__name__)

dp = Dispatcher()

@dp.error()
async def error_handler(event: ErrorEvent, state: FSMContext = None):
    logger.info("Critical error caused by %s", event.exception)
    
    if state:
        await state.clear()
    
    # Проверяем, есть ли возможность ответить пользователю
    update = event.update
    
    # Пытаемся ответить в зависимости от типа обновления
    try:
        if update.message:
            await update.message.answer("Что-то пошло не так... Попробуйте заново")
        elif update.callback_query:
            await update.callback_query.message.answer("Что-то пошло не так... Попробуйте заново")
            await update.callback_query.answer()  # Закрываем уведомление
        elif update.inline_query:
            # Для инлайн запросов можно ответить через result
            pass
        elif update.chat_member:
            # Для обновлений чат-мембера
            pass
        # Добавьте другие типы обновлений по необходимости
    except Exception as e:
        logger.error(f"Failed to send error message: {e}")


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    bot = Bot(token=settings.BOT_TOKEN)
    scheduler.start()

    scheduler.add_job(
        player_service.complete_unpublishing, "interval", hours=24, args=[bot]
    )
    scheduler.add_job(
        clan_service.complete_unpublishing, "interval", hours=24, args=[bot]
    )

    dp['scheduler'] = scheduler

    dp.include_router(start_router)

    for router in player_routers:
        dp.include_router(router)

    for router in clan_routers:
        dp.include_router(router)

    for router in fit_routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())