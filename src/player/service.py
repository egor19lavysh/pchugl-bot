from src.player.models import Player
from src.player.repository import repository
from src.player.keyboards import publish_again
from src.utils import is_subscriber, PLAYER_TEMPLATE
from aiogram import Bot
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class PlayerService:

    async def create_player(self, **values) -> Player | None:
        """
        Передает в репозиторий значения для создания анкеты
        """
        player = await repository.create_player(**values)
        return player

    async def get_player(self, user_id: int) -> list[Player]:
        """
        Получает от репозитория все анкеты игрока (от 1 до 5)
        """
        player_profiles = await repository.get_player(user_id=user_id)
        return player_profiles
    
    async def get_player_by_id(self, player_id: int) -> Player | None:
        """
        Получает от репозитория анкету игрока по ее id
        """
        player = await repository.get_player_by_id(player_id=player_id)
        return player

    
    async def get_players(self) -> list[Player]:
        """
        Получает от репозитория все анкеты всех игроков
        """
        player_profiles = await repository.get_players()
        return player_profiles
    
    async def update_player(self, player_id: int, field_name: str, value: str | int | bool | datetime | None) -> Player | None:
        """
        Обновляет поле в анкете игрока (если такая есть), если такое поле есть
        """
        if field_name not in Player.__table__.c:
            raise ValueError(f"Неизвестное поле для Player: {field_name}")
        
        player = None
        if await repository.get_player_by_id(player_id=player_id):
            player = await repository.update_field(player_id=player_id, field_name=field_name, value=value)

        return player

    async def delete_player(self, player_id: int) -> None:
        """
        Удаляет анкету игрока, если такая есть
        """
        if await repository.get_player_by_id(player_id=player_id):
            await repository.delete_player(player_id=player_id)

    async def can_register(self, bot: Bot, user_id: int) -> dict:
        """
        Узнает, есть ли у пользователя возможность зарегистрировать еще одну анкету.
        """
        answer = {}

        if not (await is_subscriber(bot=bot, user_id=user_id)):
            max_profiles_num = 1
            answer["msg"] = "Вы можете увеличить количество своих регистраций до 5, если подпишитесь на канал @pcheloteka"
        else:
            max_profiles_num = 5

        profiles = await repository.get_player(user_id=user_id)

        answer["can_register"] = max_profiles_num - len(profiles) > 0

        return answer
    
    async def get_player_info(self, player_id: int) -> str | None:
        """
        Возвращает верстку для просмотра профиля игрока
        """
        if player := await self.get_player_by_id(player_id=player_id):
            return PLAYER_TEMPLATE.format(
                nickname=player.nickname,
                tg_tag= '@' + player.tg_tag if player.tg_tag else "не указан",
                level=player.level,
                account_strength=player.account_strength,
                language=player.language,
                hydra=player.requirements_hydra,
                himera=player.requirements_himera,
                lkv=player.requirements_lkv,
                sieges=player.sieges_league
            )
        return None
    
    async def is_published(self, player_id: int) -> bool:
        """
        Проверяет, опубликована ли анкета
        """
        if player := await self.get_player_by_id(player_id=player_id):
            return player.is_published
    
    async def publish_player(self, apscheduler: AsyncIOScheduler, bot: Bot, player_id: int) -> int | None:
        """
        Публикует анкету игрока. 
        Если пользователь подписан на тг-канал, то публикуется на 7 дней, иначе на 1 день.
        Возвращает число дней, на сколько опубликована анкета
        Также планирует снятие с публикации анкеты.
        """
        if player := await self.get_player_by_id(player_id=player_id):

            if await is_subscriber(bot=bot, user_id=player.user_id):
                days = 7
            else:
                days = 1
                
            interval = timedelta(days=days)
            expiration_date = datetime.now() + interval

            try:
                await self.schedule_unpublish(apscheduler=apscheduler,
                                            time=expiration_date,
                                            bot=bot,
                                            user_id=player.user_id,
                                            player_id=player_id)
            except Exception as e:
                print(e)

            await service.update_player(player_id=player_id, field_name="is_published", value=True)
            await service.update_player(player_id=player_id, field_name="expiration_date", value=expiration_date)
            return days

    
    async def publish_players(self, apscheduler: AsyncIOScheduler, bot: Bot, user_id: int) -> None:
        """
        Публикует все анкеты пользователя.
        """
        if players := await self.get_player(user_id=user_id):
            for player in players:
                if not (await self.is_published(player_id=player.id)):
                    await self.publish_player(apscheduler=apscheduler, bot=bot, player_id=player.id)

    async def unpublish_player(self, player_id: int) -> None:
        """
        Снимает анкету пользователя с публикации.
        """
        if await self.get_player_by_id(player_id=player_id):
            await service.update_player(player_id=player_id, field_name="is_published", value=False)
            await service.update_player(player_id=player_id, field_name="expiration_date", value=None)

    async def unpublish_player_with_scheduler(self, bot: Bot, user_id: int, player_id: int) -> None:
        """
        Снимает анкету пользователя с публикации с помощью планировщика
        """
        if player := await self.get_player_by_id(player_id=player_id):
            if player.is_published:
                await self.unpublish_player(player_id=player_id)
                await bot.send_message(chat_id=user_id, text=f"Ваша анкета {player.title} снята с публикации", reply_markup=await publish_again(player_id=player_id))


    async def schedule_unpublish(self, apscheduler: AsyncIOScheduler,
                                        time: datetime,
                                        bot: Bot, 
                                        user_id: int,
                                        player_id):
        """
        Планирует снятие публикации анкеты пользователя через какое-то время
        """
        apscheduler.add_job(
            self.unpublish_player_with_scheduler,
            trigger="date",
            run_date=time,
            kwargs={
                "bot": bot,
                "user_id": user_id,
                "player_id": player_id
            }
        )

    async def complete_unpublishing(self, bot: Bot) -> None:
        """
        Проходит и проверяет все анкеты на случай, если срок публикации истек, но анкета все еще опубликована
        (планировщик по какой-то причине не сработал)
        """
        players = await self.get_players()
        now = datetime.now()
        for player in players:
            if player.is_published and player.expiration_date and now > player.expiration_date:
                await self.unpublish_player(player_id=player.id)
                await bot.send_message(chat_id=player.user_id, text=f"Ваша анкета {player.title} снята с публикации", reply_markup=await publish_again(player_id=player.id))


            


service = PlayerService()