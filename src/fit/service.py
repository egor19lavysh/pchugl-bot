from src.player.repository import repository as player_repository
from src.clan.repository import repository as clan_repository
from src.player.service import service as player_service
from src.clan.service import service as clan_service
from src.player.models import Player
from src.clan.models import Clan
from src.fit.models import Review
from src.database import get_async_session
from sqlalchemy import select
from aiogram import Bot
import logging

logger = logging.getLogger(__name__)


class FitService:

    async def filter_players(self, user_id: int, filters: dict[str, str | int | bool | None]) -> list[Player]:
        result = await player_repository.get_players_by_fields(user_id=user_id, filters=filters)
        return result
    
    async def filter_clans(self, user_id: int, filters: dict[str, str | int | bool | None]) -> list[Player]:
        result = await clan_repository.get_clans_by_fields(user_id=user_id, filters=filters)
        return result
    
    async def get_profile(self, entity: str, profile_id: int) -> Player | Clan | None:
        if entity == "player":
            return await player_service.get_player_by_id(player_id=profile_id)
        elif entity == "clan":
            return await clan_service.get_clan_by_id(clan_id=profile_id)
        else:
            return None
    
    async def get_info(self, profile: Player | Clan) -> str:
        if isinstance(profile, Player):
            info = await player_service.get_player_info(player_id=profile.id) or ""
            # attach average rating if exists
            avg, count = await self.get_average_rating(entity="player", profile_id=profile.id)
            if avg is not None:
                info = f"{info}\nРейтинг: {avg:.2f}⭐️ ({count} отзывов)"
            return info
        elif isinstance(profile, Clan):
            info = await clan_service.get_clan_info(clan_id=profile.id) or ""
            avg, count = await self.get_average_rating(entity="clan", profile_id=profile.id)
            if avg is not None:
                info = f"{info}\nРейтинг: {avg:.2f}⭐️ ({count} отзывов)"
            return info
        else:
            raise Exception("Неправильный тип данных")

    async def get_average_rating(self, entity: str, profile_id: int) -> tuple[float | None, int]:
        """
        Возвращает кортеж (average, count) для всех отзывов по анкете.
        Если отзывов нет, возвращает (None, 0).
        """
        reviews = await self.get_reviews(entity=entity, profile_id=profile_id)
        if not reviews:
            return None, 0
        total = 0
        count = 0
        for r in reviews:
            try:
                total += int(r.score)
                count += 1
            except Exception:
                continue
        if count == 0:
            return None, 0
        return total / count, count

    async def create_review(self, entity: str, profile_id: int, score: int, text: str,  reviewer: str = None) -> Review | None:
        profile = await self.get_profile(entity=entity, profile_id=profile_id)

        if not profile:
            return None

        async with get_async_session() as session:
            review = Review(
                reviewer=reviewer,
                score=score,
                text=text,
                player_id=profile_id if entity == "player" else None,
                clan_id=profile_id if entity == "clan" else None,
            )
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review

    async def get_reviews(self, entity: str, profile_id: int) -> list[Review]:
        async with get_async_session() as session:
            if entity == "player":
                stmt = select(Review).where(Review.player_id == profile_id)
            elif entity == "clan":
                stmt = select(Review).where(Review.clan_id == profile_id)
            else:
                return []

            result = await session.execute(stmt)
            return result.scalars().all()

    async def notificate_user(self, bot: Bot, profile_id: int, entity: str, msg: str) -> None:
        try:
            profile = await self.get_profile(entity=entity, profile_id=profile_id)
            await bot.send_message(chat_id=profile.user_id, text=msg)
        except Exception as e:
            logger.info(f"Бот пытался отправить сообщение пользователю {entity}_{profile_id}, но не смог из-за {e}")
        



service = FitService()