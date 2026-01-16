import logging
import os
import sys

from dotenv import load_dotenv

from bot.discord_client import VoiceNotifyClient
from bot.telegram_client import TelegramNotifier

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not all([discord_token, telegram_token, telegram_chat_id]):
        logger.error(
            "Missing required environment variables. "
            "Please set DISCORD_BOT_TOKEN, TELEGRAM_BOT_TOKEN, and TELEGRAM_CHAT_ID"
        )
        sys.exit(1)

    assert discord_token is not None
    assert telegram_token is not None
    assert telegram_chat_id is not None

    telegram_notifier = TelegramNotifier(telegram_token, telegram_chat_id)
    discord_client = VoiceNotifyClient(telegram_notifier)

    logger.info("Starting Discord bot...")
    discord_client.run(discord_token)


if __name__ == "__main__":
    main()
