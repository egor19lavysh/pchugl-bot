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
from src.clan.handlers import routers as clan_routers
from src.player.service import service as player_service
from src.clan.service import service as clan_service


dp = Dispatcher()


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
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

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())