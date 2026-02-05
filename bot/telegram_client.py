import logging

from telegram import Bot

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str) -> None:
        self.bot = Bot(token=token)

    async def send_notification(
        self,
        username: str,
        channel: str,
        server_name: str,
        chat_id: str,
        guild_id: int,
        channel_id: int,
        telegram_username: str | None = None,
    ) -> None:
        channel_url = f"https://discord.com/channels/{guild_id}/{channel_id}"
        display_name = f"@{telegram_username}" if telegram_username else username
        message = f'{display_name} joined <a href="{channel_url}">#{channel}</a>'
        try:
            await self.bot.send_message(
                chat_id=chat_id, text=message, parse_mode="HTML"
            )
            logger.info("Sent Telegram notification to %s: %s", chat_id, message)
        except Exception as e:
            logger.error("Failed to send Telegram notification: %s", e)
