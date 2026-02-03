import logging

from telegram import Bot

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str) -> None:
        self.bot = Bot(token=token)

    async def send_notification(
        self, username: str, channel: str, server_name: str, chat_id: str
    ) -> None:
        message = f"@{username} joined #{channel} on {server_name} (Discord)"
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
            logger.info("Sent Telegram notification to %s: %s", chat_id, message)
        except Exception as e:
            logger.error("Failed to send Telegram notification: %s", e)
