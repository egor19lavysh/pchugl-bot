from .models import Clan
from src.database import get_async_session
from sqlalchemy import select, update, delete


class ClanRepository:

    async def create_clan(self, 
                            user_id: int,
                            title: str,
                            name: str,
                            tg_tag: str | None,
                            photo: str | None,
                            level: int,
                            language: str,
                            sieges_league: int,
                            requirements_hydra: int,
                            requirements_himera: int,
                            requirements_lkv: int,
                            clan_tag: str | None) -> Clan:
        async with get_async_session() as session:
            """
            Создает нового игрока в базе данных и возвращает его.
            """
            clan = Clan(user_id=user_id,
                            title=title, 
                            name=name, 
                            tg_tag=tg_tag, 
                            level=level, 
                            photo=photo,
                            language=language, 
                            sieges_league=sieges_league, 
                            requirements_hydra=requirements_hydra, 
                            requirements_himera=requirements_himera, 
                            requirements_lkv=requirements_lkv,
                            clan_tag=clan_tag)
            session.add(clan)
            await session.commit()
            await session.refresh(clan)
            return clan
        
    async def get_all_clans(self) -> list[Clan]:
        """
        Получает вообще все анкеты пользователей
        """
        async with get_async_session() as session:
            result = await session.execute(select(Clan))
            return result.scalars().all()

    async def get_clans(self, user_id: int) -> list[Clan]:
        """
        Получает всех игроков из базы данных
        """
        async with get_async_session() as session:
            result = await session.execute(select(Clan).where(Clan.user_id != user_id))
            return result.scalars().all()
        
    async def get_clans_by_fields(self, user_id: int, filters: dict[str, str | int | bool | None]) -> list[Clan]:
        """
        Получает список игроков, отфильтрованных по набору полей и значений.
        """
        if not filters:
            return await self.get_clans(user_id=user_id)

        invalid_fields = [field for field in filters if field not in Clan.__table__.columns]
        if invalid_fields:
            raise ValueError(f"Недопустимые поля фильтрации: {', '.join(invalid_fields)}")

        async with get_async_session() as session:
            stmt = select(Clan)
            for field_name, value in filters.items():
                column = getattr(Clan, field_name)
                if value is not None: #Уеб...ские требования заказчика
                    if field_name in ("requirements_hydra", "requirements_himera"):
                        if value == 1:
                            stmt = stmt.where(column == value)
                        else:
                            stmt = stmt.where(column >= value)
                    elif field_name  == "requirements_lkv":
                        if value == 100:
                            stmt = stmt.where(column == value)
                        else:
                            stmt = stmt.where(column >= value)
                    elif field_name == "sieges_league":
                        if value == 5:
                            stmt = stmt.where(column == value)
                        else:
                            stmt = stmt.where(column >= value)
                    else:
                        stmt = stmt.where(column == value)
                    

            
            stmt = stmt.where(Clan.user_id != user_id)
            stmt = stmt.where(Clan.is_published == True)

            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_clan(self, user_id: int) -> list[Clan]:
        """
        Получает все анкеты игрока (от 1 до 5).
        """
        async with get_async_session() as session:
            result = await session.execute(select(Clan).where(Clan.user_id == user_id))
            return result.scalars().all()
        
    async def get_clan_by_id(self, clan_id: int) -> Clan | None:
        """
        Получает анкету игрока по его ID.
        """
        async with get_async_session() as session:
            result = await session.execute(select(Clan).where(Clan.id == clan_id))
            return result.scalar_one_or_none()
        
    async def update_field(self, clan_id: int, field_name: str, value: str | int | None) -> Clan | None:
        """
        Обновляет указанное поле в анкете игрока и возвращает обновленную анкету.
        """
        async with get_async_session() as session:
            await session.execute(
                    update(Clan).where(Clan.id == clan_id).values({field_name: value})
                )
            await session.commit()
        return await self.get_clan_by_id(clan_id)
    
    async def delete_clan(self, clan_id: int) -> None:
        """
        Удаляет анкету игрока по его ID.
        """
        async with get_async_session() as session:
            await session.execute(delete(Clan).where(Clan.id == clan_id))
            await session.commit()

repository = ClanRepository()

        
    