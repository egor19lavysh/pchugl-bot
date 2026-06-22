from .handlers import router
from .player import router as player_router
from .clan import router as clan_router
from .create_review import router as create_review_router
from .list_review import router as list_review_router


routers = [router, player_router, clan_router, create_review_router, list_review_router]