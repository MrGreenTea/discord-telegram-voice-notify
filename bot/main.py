import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from bot.discord_client import VoiceNotifyClient
from bot.telegram_client import TelegramNotifier
from bot.config_models import Config

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent.parent / "config.json"


def main() -> None:
    load_dotenv()

    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not all([discord_token, telegram_token]):
        logger.error(
            "Missing required environment variables. "
            "Please set DISCORD_BOT_TOKEN and TELEGRAM_BOT_TOKEN"
        )
        sys.exit(1)

    if not CONFIG_PATH.exists():
        logger.error("Config file not found: %s", CONFIG_PATH)
        sys.exit(1)

    try:
        with open(CONFIG_PATH) as f:
            config = Config.model_validate_json(f.read())
    except Exception as e:
        logger.error("Failed to parse config: %s", e)
        sys.exit(1)

    assert discord_token is not None
    assert telegram_token is not None

    telegram_notifier = TelegramNotifier(telegram_token)
    discord_client = VoiceNotifyClient(telegram_notifier, config)

    logger.info("Starting Discord bot...")
    discord_client.run(discord_token)


if __name__ == "__main__":
    main()
