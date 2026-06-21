from src.player.repository import repository as player_repository
from src.clan.repository import repository as clan_repository
from src.player.service import service as player_service
from src.clan.service import service as clan_service
from src.player.models import Player
from src.clan.models import Clan
from src.fit.models import Review
from src.database import get_async_session
from sqlalchemy import select


class FitService:

    async def filter_players(self, user_id: int, filters: dict[str, str | int | bool | None]) -> list[Player]:
        result = await player_repository.get_players_by_fields(user_id=user_id, filters=filters)
        return result
    
    async def filter_clans(self, user_id: int, filters: dict[str, str | int | bool | None]) -> list[Player]:
        result = await clan_repository.get_clans_by_fields(user_id=user_id, filters=filters)
        return result
    
    async def get_info(self, profile: Player | Clan) -> str:
        if isinstance(profile, Player):
            return await player_service.get_player_info(player_id=profile.id)
        elif isinstance(profile, Clan):
            return await clan_service.get_clan_info(clan_id=profile.id)
        else:
            raise Exception("Неправильный тип данных")

    async def create_review(self, entity: str, profile_id: int, score: int, text: str) -> Review | None:
        if entity == "player":
            profile = await player_service.get_player_by_id(player_id=profile_id)
        elif entity == "clan":
            profile = await clan_service.get_clan_by_id(clan_id=profile_id)
        else:
            return None

        if not profile:
            return None

        async with get_async_session() as session:
            review = Review(
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


service = FitService()