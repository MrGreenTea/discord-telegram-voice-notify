from pydantic import BaseModel, Field


class ChannelMapping(BaseModel):
    discord_channel: str
    telegram_chat_id: str


class UserMapping(BaseModel):
    discord_user_id: int
    telegram_username: str
    comment: str | None = None


class Config(BaseModel):
    default_telegram_chat_id: str
    mappings: list[ChannelMapping] = Field(default_factory=list)
    user_mappings: list[UserMapping] = Field(default_factory=list)
    debounce_seconds: int = 60
