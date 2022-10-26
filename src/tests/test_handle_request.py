import pytest
from nonebug import App

from . import MyTest
from .templates import *


class TestAutoApproveFriendAdd(MyTest):
    env = {
        "onebot_monitor_auto_approve_friend_add_request": "true"
    }

    @pytest.mark.asyncio
    async def test(self, app: App):
        from nonebot_plugin_onebot_monitor.handle_request import friend_add
        from nonebot.adapters.onebot.v11 import Bot

        async with app.test_matcher(friend_add) as ctx:
            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, friend_request_event())
            ctx.should_call_api("set_friend_add_request", data={
                "flag": FLAG,
                "approve": True,
                'remark': ''
            }, result={})


class TestAutoApproveGroupInvite(MyTest):
    env = {
        "onebot_monitor_auto_approve_group_invite_request": "true"
    }

    @pytest.mark.asyncio
    async def test(self, app: App):
        from nonebot_plugin_onebot_monitor.handle_request import group_invite
        from nonebot.adapters.onebot.v11 import Bot

        async with app.test_matcher(group_invite) as ctx:
            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, group_request_event())
            ctx.should_call_api("set_group_add_request", data={
                "flag": FLAG,
                "sub_type": "invite",
                "approve": True
            }, result={})


class TestForwardRequest(MyTest):
    env = {
        "onebot_monitor_request_forward_to": str(FORWARD_TO)
    }

    @pytest.mark.asyncio
    async def test_friend_add(self, app: App):
        from nonebot_plugin_onebot_monitor.handle_request import friend_add
        from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

        async with app.test_matcher(friend_add) as ctx:
            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, friend_request_event())
            ctx.should_call_api("send_private_msg", data={
                "user_id": FORWARD_TO,
                "message": Message(MessageSegment.text(f"收到来自用户{USER_ID}的好友申请。回复“同意”或“拒绝”处理此申请。"))
            }, result={
                "message_id": MESSAGE_ID
            })

        from nonebot_plugin_onebot_monitor.handle_request import context, latest_request

        assert MESSAGE_ID in context
        assert context[MESSAGE_ID] == latest_request[str(SELF_ID)]

    @pytest.mark.asyncio
    async def test_group_invite(self, app: App):
        from nonebot_plugin_onebot_monitor.handle_request import group_invite
        from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

        async with app.test_matcher(group_invite) as ctx:
            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, group_request_event())
            ctx.should_call_api("send_private_msg", data={
                "user_id": FORWARD_TO,
                "message": Message(MessageSegment.text(f"收到来自群{GROUP_ID}的入群邀请。回复“同意”或“拒绝”处理此申请。"))
            }, result={
                "message_id": MESSAGE_ID
            })

        from nonebot_plugin_onebot_monitor.handle_request import context, latest_request

        assert MESSAGE_ID in context
        assert context[MESSAGE_ID] == latest_request[str(SELF_ID)]


class TestOperation(MyTest):
    env = {
        "onebot_monitor_request_forward_to": str(FORWARD_TO)
    }

    @pytest.mark.asyncio
    async def test_approve(self, app: App):
        from nonebot_plugin_onebot_monitor.handle_request import approve_matcher
        from nonebot.adapters.onebot.v11 import Bot

        from nonebot_plugin_onebot_monitor.handle_request import context, latest_request

        req = group_request_event()
        context[MESSAGE_ID] = req
        latest_request[str(SELF_ID)] = req

        async with app.test_matcher(approve_matcher) as ctx:
            message_event = private_message_event("同意")

            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, message_event)
            ctx.should_call_api("set_group_add_request", data={
                "flag": FLAG,
                "sub_type": "invite",
                "approve": True
            }, result={})
            ctx.should_call_send(message_event, "成功同意请求", result={
                "message_id": MESSAGE_ID_3
            })

        assert str(SELF_ID) not in latest_request

    @pytest.mark.asyncio
    async def test_reject(self, app: App):
        from nonebot_plugin_onebot_monitor.handle_request import reject_matcher
        from nonebot.adapters.onebot.v11 import Bot

        from nonebot_plugin_onebot_monitor.handle_request import context, latest_request

        req = group_request_event()
        context[MESSAGE_ID] = req
        latest_request[str(SELF_ID)] = req

        async with app.test_matcher(reject_matcher) as ctx:
            message_event = private_message_event("拒绝")

            bot = ctx.create_bot(self_id=str(SELF_ID), base=Bot)
            ctx.receive_event(bot, message_event)
            ctx.should_call_api("set_group_add_request", data={
                "flag": FLAG,
                "sub_type": "invite",
                "approve": False,
                "reason": ""
            }, result={})
            ctx.should_call_send(message_event, "成功拒绝请求", result={
                "message_id": MESSAGE_ID_3
            })

        assert str(SELF_ID) not in latest_request
