from nonebot import on_request, logger
from nonebot.adapters.onebot.v11 import Bot, GroupRequestEvent, Event
from nonebot.adapters.onebot.v11 import FriendRequestEvent

from .config import conf

if conf.auto_approve_friend_add_request:
    async def _friend_add_request(event: Event) -> bool:
        return isinstance(event, FriendRequestEvent)


    friend_add = on_request(_friend_add_request, priority=10)


    @friend_add.handle()
    async def on_friend_add(bot: Bot, event: FriendRequestEvent):
        await bot.set_friend_add_request(flag=event.flag, approve=True)
        logger.success(f"auto approved friend add request from {event.user_id}")

if conf.auto_approve_group_invite_request:
    async def _group_invite_request(event: Event) -> bool:
        return isinstance(event, GroupRequestEvent) and event.sub_type == "invite"


    group_invite = on_request(_group_invite_request, priority=10)


    @group_invite.handle()
    async def on_group_invite(bot: Bot, event: GroupRequestEvent):
        await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)
        logger.success(f"auto approved group {event.group_id} invite request from {event.user_id}")
