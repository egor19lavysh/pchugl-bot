from src.player.models import Player
from src.player.repository import repository, PlayerRepository
from src.utils import is_subscriber, PLAYER_TEMPLATE
from aiogram import Bot


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
    
    async def update_player(self, player_id: int, field_name: str, value: str | int | None) -> Player | None:
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

            

service = PlayerService()