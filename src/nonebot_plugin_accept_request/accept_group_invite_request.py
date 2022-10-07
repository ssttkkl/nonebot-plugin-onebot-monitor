from asyncio import Event

from nonebot import on_request, logger
from nonebot.adapters.onebot.v11 import Bot, GroupRequestEvent


async def _group_invite_request(event: Event) -> bool:
    return isinstance(event, GroupRequestEvent) and event.sub_type == "invite"


group_invite = on_request(_group_invite_request, priority=10, block=True)


@group_invite.handle()
async def on_group_invite(bot: Bot, event: GroupRequestEvent):
    await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)
    logger.success(f"accepted group {event.group_id} invite request from onebot:{event.user_id}")
