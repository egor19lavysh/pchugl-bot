from .models import Player
from src.database import get_async_session
from sqlalchemy import select, update, delete


class PlayerRepository:

    async def create_player(self, 
                            user_id: int,
                            title: str,
                            nickname: str,
                            tg_tag: str | None,
                            level: int,
                            account_strength: int,
                            language: str,
                            sieges_league: str,
                            requirements_hydra: str,
                            requirements_himera: str,
                            requirements_lkv: str) -> Player:
        async with get_async_session() as session:
            """
            Создает нового игрока в базе данных и возвращает его.
            """
            player = Player(user_id=user_id,
                            title=title, 
                            nickname=nickname, 
                            tg_tag=tg_tag, 
                            level=level, 
                            account_strength=account_strength, 
                            language=language, 
                            sieges_league=sieges_league, 
                            requirements_hydra=requirements_hydra, 
                            requirements_himera=requirements_himera, 
                            requirements_lkv=requirements_lkv)
            session.add(player)
            await session.commit()
            await session.refresh(player)
            return player

    async def get_players() -> list[Player]:
        """
        Получает всех игроков из базы данных
        """
        async with get_async_session() as session:
            result = await session.execute(select(Player))
            return result.scalars().all()

    async def get_player(self, user_id: int) -> list[Player]:
        """
        Получает все анкеты игрока (от 1 до 5).
        """
        async with get_async_session() as session:
            result = await session.execute(select(Player).where(Player.user_id == user_id))
            return result.scalars().all()
        
    async def get_player_by_id(self, player_id: int) -> Player | None:
        """
        Получает анкету игрока по его ID.
        """
        async with get_async_session() as session:
            result = await session.execute(select(Player).where(Player.id == player_id))
            return result.scalar_one_or_none()
        
    async def update_field(self, player_id: int, field_name: str, value: str | int | None) -> Player | None:
        """
        Обновляет указанное поле в анкете игрока и возвращает обновленную анкету.
        """
        # Prevent updating arbitrary SQL identifiers
        if field_name not in Player.__table__.c:
            raise ValueError(f"Unknown field for Player: {field_name}")

        async with get_async_session() as session:
            await session.execute(
                    update(Player).where(Player.id == player_id).values({field_name: value})
                )
            await session.commit()
        return self.get_player_by_id(player_id)
    
    async def delete_player(self, player_id: int) -> None:
        """
        Удаляет анкету игрока по его ID.
        """
        async with get_async_session() as session:
            await session.execute(delete(Player).where(Player.id == player_id))
            await session.commit()

repository = PlayerRepository()

        
    