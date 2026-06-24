import random
import asyncio
from faker import Faker
from src.clan.repository import repository as clan_repository
from src.fit.service import service as fit_service
from src.player.repository import repository as player_repository
from src.database import get_async_session


faker = Faker()

LANGUAGES = ["RU", "UA", "EN", "Другое"]
REQUIREMENTS_OPTIONS = [1, 4, 8, 12, 16, 20, 24, 28]
LKV_OPTIONS = [0, 100, 200, 300, 400, 500, 600, 700, 800]
SIEGES_OPTIONS = [5, 6, 7, 8]
CLAN_LEVEL_OPTIONS = ["20", "21", "22", "23", "24", "25", "26", "27"]


def _random_tg_tag() -> str | None:
    if random.random() < 0.2:
        return None
    return faker.user_name()


def _random_photo() -> str | None:
    if random.random() < 0.3:
        return None
    return faker.image_url(width=640, height=360)


def _random_reviewer() -> str | None:
    if random.random() < 0.3:
        return None
    return faker.user_name()


async def create_player():
    """Создаёт рандомную анкету игрока и сохраняет её в базе."""
    await player_repository.create_player(
        user_id=faker.unique.random_int(min=100000000, max=999999999),
        title=faker.sentence(nb_words=3).strip("."),
        nickname=faker.user_name(),
        tg_tag=_random_tg_tag(),
        level=random.randint(1, 100),
        account_strength=random.randint(1, 100),
        language=random.choice(LANGUAGES),
        sieges_league=random.choice(SIEGES_OPTIONS),
        requirements_hydra=random.choice(REQUIREMENTS_OPTIONS),
        requirements_himera=random.choice(REQUIREMENTS_OPTIONS),
        requirements_lkv=random.choice(LKV_OPTIONS),
        photo=None
    )

async def publish_all_players():
    players = await player_repository.get_all_players()
    for p in players:
        await player_repository.update_field(player_id=p.id, field_name="is_published", value=True)

async def publish_all_clans():
    clans = await clan_repository.get_all_clans()
    for c in clans:
        await clan_repository.update_field(clan_id=c.id, field_name="is_published", value=True)

async def create_players(count: int = 100):
    """Создаёт несколько рандомных анкет игроков."""
    for _ in range(count):
        try:
            await create_player()
        except Exception as e:
            continue


async def create_clan():
    """Создаёт рандомную анкету клана и сохраняет её в базе."""
    await clan_repository.create_clan(
        user_id=faker.unique.random_int(min=100000000, max=999999999),
        title=faker.sentence(nb_words=3).strip("."),
        name=faker.company(),
        tg_tag=_random_tg_tag(),
        clan_tag="tag",
        photo=None,
        level=random.choice(CLAN_LEVEL_OPTIONS),
        language=random.choice(LANGUAGES),
        sieges_league=random.choice(SIEGES_OPTIONS),
        requirements_hydra=random.choice(REQUIREMENTS_OPTIONS),
        requirements_himera=random.choice(REQUIREMENTS_OPTIONS),
        requirements_lkv=random.choice(LKV_OPTIONS)
    )


async def create_clans(count: int = 50):
    """Создаёт несколько рандомных анкет кланов."""
    for _ in range(count):
        await create_clan()
            


async def create_review(
    entity: str,
    profile_id: int,
    score: int | None = None,
    text: str | None = None,
    reviewer: str | None = None,
):
    """Создаёт один отзыв для игрока или клана."""
    if score is None:
        score = random.randint(1, 5)
    if text is None:
        text = faker.sentence(nb_words=random.randint(8, 20))
    if reviewer is None:
        reviewer = _random_reviewer()

    return await fit_service.create_review(
        entity=entity,
        profile_id=profile_id,
        score=score,
        text=text,
        reviewer=reviewer,
    )


async def create_reviews(count: int = 200, entities: list[str] | None = None):
    """Создаёт несколько рандомных отзывов игрокам и кланам."""
    if entities is None:
        entities = ["player", "clan"]

    players = await player_repository.get_all_players()
    clans = await clan_repository.get_all_clans()
    if not players and not clans:
        return

    for _ in range(count):
        entity = random.choice(entities)
        if entity == "player" and players:
            profile_id = random.choice(players).id
        elif entity == "clan" and clans:
            profile_id = random.choice(clans).id
        elif players:
            entity = "player"
            profile_id = random.choice(players).id
        else:
            entity = "clan"
            profile_id = random.choice(clans).id

        await create_review(entity=entity, profile_id=profile_id)


from sqlalchemy import delete
from src.fit.models import Review
from src.player.models import Player
from src.clan.models import Clan


async def drop_all():
    async with get_async_session() as session:
        await session.execute(delete(Review))
        await session.execute(delete(Player))
        await session.execute(delete(Clan))
        await session.commit()

async def main():
    await drop_all()
    #await create_players()
    #await publish_all_players()
    #await create_clans()
    #await publish_all_clans()
    #await create_reviews()

if __name__ == "__main__":
    asyncio.run(main())