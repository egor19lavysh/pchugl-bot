from aiogram import Bot, types
import io
from datetime import datetime

from src.player.repository import repository as player_repository
from src.clan.repository import repository as clan_repository
from src.fit.service import service as fit_service


class AdminService:
    async def export_profiles_excel(self, bot: Bot, user_id: int) -> None:
        """
        Экспорт всех анкет игроков и кланов в Excel-файл и отправка пользователю.
        """
        players = await player_repository.get_all_players()
        clans = await clan_repository.get_all_clans()

        try:
            from openpyxl import Workbook
        except Exception as e:
            raise RuntimeError("openpyxl is required to export excel files. Install it with 'pip install openpyxl'") from e

        wb = Workbook()

        # Players sheet
        ws_p = wb.active
        ws_p.title = "Players"
        headers_p = [
            "id", "user_id", "title", "nickname", "tg_tag", "level", "account_strength",
            "language", "sieges_league", "requirements_hydra", "requirements_himera", "requirements_lkv",
            "is_published", "expiration_date", "avg_rating", "review_count"
        ]
        ws_p.append(headers_p)

        for p in players:
            avg, count = await fit_service.get_average_rating(entity="player", profile_id=p.id)
            avg_val = f"{avg:.2f}" if avg is not None else ""
            row = [
                p.id,
                p.user_id,
                getattr(p, "title", ""),
                getattr(p, "nickname", ""),
                getattr(p, "tg_tag", "") or "",
                getattr(p, "level", ""),
                getattr(p, "account_strength", ""),
                getattr(p, "language", ""),
                getattr(p, "sieges_league", ""),
                getattr(p, "requirements_hydra", ""),
                getattr(p, "requirements_himera", ""),
                getattr(p, "requirements_lkv", ""),
                getattr(p, "is_published", ""),
                str(getattr(p, "expiration_date", "")) if getattr(p, "expiration_date", None) else "",
                avg_val,
                count,
            ]
            ws_p.append(row)

        # Clans sheet
        ws_c = wb.create_sheet("Clans")
        headers_c = [
            "id", "user_id", "title", "name", "tg_tag", "photo", "level",
            "language", "sieges_league", "requirements_hydra", "requirements_himera", "requirements_lkv",
            "is_published", "expiration_date", "avg_rating", "review_count"
        ]
        ws_c.append(headers_c)

        for c in clans:
            avg, count = await fit_service.get_average_rating(entity="clan", profile_id=c.id)
            avg_val = f"{avg:.2f}" if avg is not None else ""
            row = [
                c.id,
                c.user_id,
                getattr(c, "title", ""),
                getattr(c, "name", ""),
                getattr(c, "tg_tag", "") or "",
                getattr(c, "photo", "") or "",
                getattr(c, "level", ""),
                getattr(c, "language", ""),
                getattr(c, "sieges_league", ""),
                getattr(c, "requirements_hydra", ""),
                getattr(c, "requirements_himera", ""),
                getattr(c, "requirements_lkv", ""),
                getattr(c, "is_published", ""),
                str(getattr(c, "expiration_date", "")) if getattr(c, "expiration_date", None) else "",
                avg_val,
                count,
            ]
            ws_c.append(row)

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)

        filename = f"profiles_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        await bot.send_document(chat_id=user_id, document=types.BufferedInputFile(buf.getvalue(), filename))


service = AdminService()