from typing import List, Optional

from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    onebot_monitor_db_conn_url: str = "sqlite+aiosqlite:///onebot_monitor.db"
    onebot_monitor_ignore: List[str] = ["notice.notify.poke"]

    onebot_monitor_auto_approve_friend_add_request: bool = False
    onebot_monitor_auto_approve_group_invite_request: bool = False

    onebot_monitor_request_forward_to: Optional[int]

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())

__all__ = ("conf", "Config")
