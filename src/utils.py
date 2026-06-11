from aiogram import Bot


async def is_subscriber(bot: Bot, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь подписчиком канала @pcheloteka.
    """
    user = await bot.get_chat_member(chat_id="@pcheloteka", user_id=user_id)
    return user.status != "left"