from nonebot import get_driver
from nonebot_plugin_sqlalchemy import DataSource

from ..config import conf

data_source = DataSource(get_driver(), conf.onebot_monitor_db_conn_url)

__all__ = ("data_source",)
