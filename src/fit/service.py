from src.player.repository import repository as player_repository
from src.clan.repository import repository as clan_repository
from src.player.service import service as player_service
from src.clan.service import service as clan_service
from src.player.models import Player
from src.clan.models import Clan


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


service = FitService()