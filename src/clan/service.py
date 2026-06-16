from src.clan.models import Clan
from src.clan.repository import repository
from src.clan.keyboards import publish_again
from src.utils import is_subscriber, CLAN_TEMPLATE
from aiogram import Bot
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class ClanService:

    async def create_clan(self, **values) -> Clan | None:
        """
        Передает в репозиторий значения для создания анкеты
        """
        clan = await repository.create_clan(**values)
        return clan

    async def get_clan(self, user_id: int) -> list[Clan]:
        """
        Получает от репозитория все анкеты игрока (от 1 до 5)
        """
        clan_profiles = await repository.get_clan(user_id=user_id)
        return clan_profiles
    
    async def get_clan_by_id(self, clan_id: int) -> Clan | None:
        """
        Получает от репозитория анкету игрока по ее id
        """
        clan = await repository.get_clan_by_id(clan_id=clan_id)
        return clan

    
    async def get_clans(self) -> list[Clan]:
        """
        Получает от репозитория все анкеты всех игроков
        """
        clan_profiles = await repository.get_clans()
        return clan_profiles
    
    async def update_clan(self, clan_id: int, field_name: str, value: str | int | bool | datetime | None) -> Clan | None:
        """
        Обновляет поле в анкете игрока (если такая есть), если такое поле есть
        """
        if field_name not in Clan.__table__.c:
            raise ValueError(f"Неизвестное поле для Clan: {field_name}")
        
        clan = None
        if await repository.get_clan_by_id(clan_id=clan_id):
            clan = await repository.update_field(clan_id=clan_id, field_name=field_name, value=value)

        return clan

    async def delete_clan(self, clan_id: int) -> None:
        """
        Удаляет анкету игрока, если такая есть
        """
        if await repository.get_clan_by_id(clan_id=clan_id):
            await repository.delete_clan(clan_id=clan_id)

    async def can_register(self, bot: Bot, user_id: int) -> dict:
        """
        Узнает, есть ли у пользователя возможность зарегистрировать еще одну анкету.
        """
        answer = {}

        if not (await is_subscriber(bot=bot, user_id=user_id)):
            max_profiles_num = 1
            answer["msg"] = "Вы можете увеличить количество своих регистраций до 20, если подпишитесь на канал @pcheloteka"
        else:
            max_profiles_num = 20

        profiles = await repository.get_clan(user_id=user_id)

        answer["can_register"] = max_profiles_num - len(profiles) > 0

        return answer
    
    async def get_clan_info(self, clan_id: int) -> str | None:
        if clan := await self.get_clan_by_id(clan_id=clan_id):
            return CLAN_TEMPLATE.format(
                name=clan.name,
                tg_tag= '@' + clan.tg_tag if clan.tg_tag else "не указан",
                level=clan.level,
                language=clan.language,
                hydra=clan.requirements_hydra,
                himera=clan.requirements_himera,
                lkv=clan.requirements_lkv,
                sieges=clan.sieges_league
            )
        return None
    
    async def is_published(self, clan_id: int) -> bool:
        """
        Проверяет, опубликована ли анкета
        """
        if clan := await self.get_clan_by_id(clan_id=clan_id):
            return clan.is_published
    
    async def publish_clan(self, apscheduler: AsyncIOScheduler, bot: Bot, clan_id: int) -> int | None:
        """
        Публикует анкету игрока. 
        Если пользователь подписан на тг-канал, то публикуется на 7 дней, иначе на 1 день.
        Возвращает число дней, на сколько опубликована анкета
        Также планирует снятие с публикации анкеты.
        """
        if clan := await self.get_clan_by_id(clan_id=clan_id):

            if await is_subscriber(bot=bot, user_id=clan.user_id):
                days = 7
            else:
                days = 1
                
            interval = timedelta(minutes=days)
            expiration_date = datetime.now() + interval

            try:
                await self.schedule_unpublish(apscheduler=apscheduler,
                                            time=expiration_date,
                                            bot=bot,
                                            user_id=clan.user_id,
                                            clan_id=clan_id)
            except Exception as e:
                print(e)

            await service.update_clan(clan_id=clan_id, field_name="is_published", value=True)
            await service.update_clan(clan_id=clan_id, field_name="expiration_date", value=expiration_date)
            return days

    
    async def publish_clans(self, apscheduler: AsyncIOScheduler, bot: Bot, user_id: int) -> None:
        """
        Публикует все анкеты пользователя.
        """
        if clans := await self.get_clan(user_id=user_id):
            for clan in clans:
                if not (await self.is_published(clan_id=clan.id)):
                    await self.publish_clan(apscheduler=apscheduler, bot=bot, clan_id=clan.id)

    async def unpublish_clan(self, clan_id: int) -> None:
        """
        Снимает анкету пользователя с публикации.
        """
        if await self.get_clan_by_id(clan_id=clan_id):
            await service.update_clan(clan_id=clan_id, field_name="is_published", value=False)
            await service.update_clan(clan_id=clan_id, field_name="expiration_date", value=None)

    async def unpublish_clan_with_scheduler(self, bot: Bot, user_id: int, clan_id: int) -> None:
        """
        Снимает анкету пользователя с публикации с помощью планировщика
        """
        if clan := await self.get_clan_by_id(clan_id=clan_id):
            if clan.is_published:
                await self.unpublish_clan(clan_id=clan_id)
                await bot.send_message(chat_id=user_id, text=f"Ваша анкета {clan.title} снята с публикации", reply_markup=await publish_again(clan_id=clan_id))


    async def schedule_unpublish(self, apscheduler: AsyncIOScheduler,
                                        time: datetime,
                                        bot: Bot, 
                                        user_id: int,
                                        clan_id):
        """
        Планирует снятие публикации анкеты пользователя через какое-то время
        """
        apscheduler.add_job(
            self.unpublish_clan_with_scheduler,
            trigger="date",
            run_date=time,
            kwargs={
                "bot": bot,
                "user_id": user_id,
                "clan_id": clan_id
            }
        )

    async def complete_unpublishing(self, bot: Bot) -> None:
        """
        Проходит и проверяет все анкеты на случай, если срок публикации истек, но анкета все еще опубликована
        (планировщик по какой-то причине не сработал)
        """
        clans = await self.get_clans()
        now = datetime.now()
        for clan in clans:
            if clan.is_published and clan.expiration_date and now > clan.expiration_date:
                await self.unpublish_clan(clan_id=clan.id)
                await bot.send_message(chat_id=clan.user_id, text=f"Ваша анкета {clan.title} снята с публикации", reply_markup=await publish_again(clan_id=clan.id))


            


service = ClanService()