import logging
import time

import discord

from bot.telegram_client import TelegramNotifier
from bot.config_models import Config

logger = logging.getLogger(__name__)


class VoiceNotifyClient(discord.Client):
    def __init__(
        self,
        telegram_notifier: TelegramNotifier,
        config: Config,
    ) -> None:
        intents = discord.Intents.default()
        intents.voice_states = True
        super().__init__(intents=intents)
        self.telegram_notifier = telegram_notifier
        self.default_chat_id = config.default_telegram_chat_id
        self.channel_mappings = {
            m.discord_channel_id: m.telegram_chat_id for m in config.mappings
        }
        self.user_mappings = {
            m.discord_user_id: m.telegram_username for m in config.user_mappings
        }
        # Track last notification time per user to prevent spam
        # Key: user_id, Value: timestamp
        self._last_notification_times: dict[int, float] = {}
        self.debounce_seconds = config.debounce_seconds

    async def on_ready(self) -> None:
        logger.info("Discord bot logged in as %s", self.user)

    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        logger.debug(
            "Voice state update: %s moved from %s (%s) to %s (%s)",
            member.display_name,
            before.channel.name if before.channel else None,
            before.channel.id if before.channel else None,
            after.channel.name if after.channel else None,
            after.channel.id if after.channel else None,
        )
        # Only trigger when user joins a voice channel (wasn't in one before)
        if before.channel is None and after.channel is not None:
            current_time = time.time()
            last_time = self._last_notification_times.get(member.id, 0)

            if current_time - last_time < self.debounce_seconds:
                logger.info(
                    "Debouncing notification for %s (last sent %.1fs ago)",
                    member.display_name,
                    current_time - last_time,
                )
                return

            username = member.display_name
            telegram_username = self.user_mappings.get(member.id)
            channel_name = after.channel.name
            channel_id = str(after.channel.id)

            logger.info(
                "User %s joined voice channel %s (ID: %s)",
                username,
                channel_name,
                channel_id,
            )

            server_name = after.channel.guild.name
            chat_id = self.channel_mappings.get(channel_id, self.default_chat_id)

            await self.telegram_notifier.send_notification(
                username,
                channel_name,
                server_name,
                chat_id,
                guild_id=after.channel.guild.id,
                channel_id=after.channel.id,
                telegram_username=telegram_username,
            )
            self._last_notification_times[member.id] = current_time
