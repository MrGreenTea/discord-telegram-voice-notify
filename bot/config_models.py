from pydantic import BaseModel, Field


class ChannelMapping(BaseModel):
    discord_channel: str
    telegram_chat_id: str


class Config(BaseModel):
    default_telegram_chat_id: str
    mappings: list[ChannelMapping] = Field(default_factory=list)
    debounce_seconds: int = 60
