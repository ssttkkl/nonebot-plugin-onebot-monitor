import pytest
from nonebug import App

from tests import MyTest
from tests.mock_data_source import MockDataSource
from tests.templates import SELF_ID, friend_request_event


class TestMonitorRequest(MyTest, MockDataSource):
    @pytest.mark.asyncio
    async def test_record(self, app: App):
        from nonebot.adapters.onebot.v11 import Bot

        from nonebot_plugin_onebot_monitor.monitor_request import monitor_request_matcher
        from nonebot_plugin_onebot_monitor.models import data_source

        req = friend_request_event()

        async with app.test_matcher(monitor_request_matcher) as ctx:
            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, req)

        data_source.session().add.assert_called_once()
