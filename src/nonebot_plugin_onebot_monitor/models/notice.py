from enum import Enum
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Integer, BigInteger, JSON, String, Enum as SqlEnum

from nonebot_plugin_onebot_monitor.models import data_source


class NoticeType(str, Enum):
    group_upload = "group_upload"
    group_admin = "group_admin"
    group_decrease = "group_decrease"
    group_increase = "group_increase"
    group_ban = "group_ban"
    friend_add = "friend_add"
    group_recall = "group_recall"
    friend_recall = "friend_recall"
    group_card = "group_card"
    offline_file = "offline_file"
    client_status = "client_status"
    essence = "essence"
    notify = "notify"


@data_source.registry.mapped
class NoticeOrm:
    __tablename__ = "notices"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    time: int = Column(BigInteger, nullable=False)
    self_id: int = Column(BigInteger, nullable=False)

    notice_type: NoticeType = Column(SqlEnum(NoticeType), nullable=False)
    sub_type: Optional[str] = Column(String)

    user_id: Optional[int] = Column(BigInteger)
    group_id: Optional[int] = Column(BigInteger)

    extra: dict = Column(JSON)
