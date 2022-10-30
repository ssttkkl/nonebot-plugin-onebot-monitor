from nonebot import get_driver, require

from ..config import conf

require("nonebot_plugin_sqlalchemy")

from nonebot_plugin_sqlalchemy import DataSource

data_source = DataSource(get_driver(), conf.onebot_monitor_db_conn_url)

__all__ = ("data_source",)
