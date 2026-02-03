import logging
from typing import Any

import discord

from bot.telegram_client import TelegramNotifier

logger = logging.getLogger(__name__)


class VoiceNotifyClient(discord.Client):
    def __init__(
        self,
        telegram_notifier: TelegramNotifier,
        config: dict[str, Any],
    ) -> None:
        intents = discord.Intents.default()
        intents.voice_states = True
        super().__init__(intents=intents)
        self.telegram_notifier = telegram_notifier
        self.default_chat_id = config["default_telegram_chat_id"]
        self.channel_mappings = {
            m["discord_channel"]: m["telegram_chat_id"] for m in config["mappings"]
        }

    async def on_ready(self) -> None:
        logger.info("Discord bot logged in as %s", self.user)

    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        logger.debug(
            "Voice state update: %s moved from %s to %s",
            member.display_name,
            before.channel.name if before.channel else None,
            after.channel.name if after.channel else None,
        )
        # Only trigger when user joins a voice channel (wasn't in one before)
        if before.channel is None and after.channel is not None:
            username = member.display_name
            channel = after.channel.name
            logger.info("User %s joined voice channel %s", username, channel)
            server_name = after.channel.guild.name
            chat_id = self.channel_mappings.get(channel, self.default_chat_id)
            await self.telegram_notifier.send_notification(
                username,
                channel,
                server_name,
                chat_id,
                guild_id=after.channel.guild.id,
                channel_id=after.channel.id,
            )
