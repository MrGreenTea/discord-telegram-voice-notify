import logging

from telegram import Bot

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str) -> None:
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_notification(self, username: str, channel: str) -> None:
        message = f"@{username} joined #{channel}"
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            logger.info("Sent Telegram notification: %s", message)
        except Exception as e:
            logger.error("Failed to send Telegram notification: %s", e)
