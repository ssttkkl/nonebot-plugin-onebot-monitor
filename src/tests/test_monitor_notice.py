import pytest
from nonebug import App

from tests import MyTest
from tests.mock_data_source import MockDataSource
from tests.mock_map_user_group import MockMapUserGroup
from tests.templates import SELF_ID, group_admin_notice_event, FORWARD_TO, MESSAGE_ID, GROUP_ID


class TestMonitorNotice(MyTest, MockDataSource):
    @pytest.mark.asyncio
    async def test_record(self, app: App):
        from nonebot.adapters.onebot.v11 import Bot

        from nonebot_plugin_onebot_monitor.monitor_notice import monitor_notice_matcher
        from nonebot_plugin_onebot_monitor.models import data_source

        req = group_admin_notice_event()

        async with app.test_matcher(monitor_notice_matcher) as ctx:
            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, req)

        data_source.session().add.assert_called_once()


class TestMonitorNoticeForward(MyTest, MockDataSource, MockMapUserGroup):
    env = {
        "onebot_monitor_forward_to": FORWARD_TO,
        "onebot_monitor_forward_notice": True
    }

    @pytest.mark.asyncio
    async def test_forward(self, app: App, patch_map_user_group):
        from nonebot_plugin_onebot_monitor import monitor_notice
        patch_map_user_group(monitor_notice)

        from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
        from nonebot_plugin_onebot_monitor.monitor_notice import monitor_notice_matcher
        from nonebot_plugin_onebot_monitor.models import data_source

        req = group_admin_notice_event()

        async with app.test_matcher(monitor_notice_matcher) as ctx:
            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, req)
            ctx.should_call_api("send_private_msg", data={
                "user_id": FORWARD_TO,
                "message": Message(MessageSegment.text(f"Bot被设置为群聊{GROUP_ID}的管理员"))
            }, result={
                "message_id": MESSAGE_ID
            })

        data_source.session().add.assert_called_once()
