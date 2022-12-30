from enum import Enum
from typing import Optional

from sqlalchemy import Column, BigInteger, Integer, String, Enum as SqlEnum, JSON
from sqlmodel.main import default_registry


class RequestType(str, Enum):
    friend = "friend"
    group = "group"


@default_registry.mapped
class RequestOrm:
    __tablename__ = "requests"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    time: int = Column(BigInteger, nullable=False)
    self_id: int = Column(BigInteger, nullable=False)

    request_type: RequestType = Column(SqlEnum(RequestType), nullable=False)
    sub_type: Optional[str] = Column(String)

    user_id: int = Column(BigInteger, nullable=False)
    group_id: Optional[int] = Column(BigInteger)

    extra: dict = Column(JSON)
