from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from src.utils import is_subscriber


router = Router()

@router.callback_query(F.data == "player")
async def player_handler(callback: CallbackQuery) -> None:
    await callback.answer()

    is_sub = await is_subscriber(callback.bot, callback.from_user.id)