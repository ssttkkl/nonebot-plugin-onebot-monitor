from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    accept_friend_add_request: bool = False
    accept_group_add_request: bool = False
    accept_group_invite_request: bool = False

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())

__all__ = ("conf", "Config")
