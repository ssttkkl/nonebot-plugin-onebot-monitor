from typing import List

from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    onebot_monitor_db_conn_url: str = "sqlite+aiosqlite:///onebot_monitor.db"

    auto_approve_friend_add_request: bool = False
    auto_approve_group_invite_request: bool = False

    onebot_monitor_ignore: List[str] = ["notice.notify.poke"]

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())

__all__ = ("conf", "Config")
