from asyncio import Event

from nonebot import on_request, logger
from nonebot.adapters.onebot.v11 import FriendRequestEvent, Bot


async def _friend_add_request(event: Event) -> bool:
    return isinstance(event, FriendRequestEvent)


friend_add = on_request(_friend_add_request, priority=10, block=True)


@friend_add.handle()
async def on_friend_add(bot: Bot, event: FriendRequestEvent):
    await bot.set_friend_add_request(flag=event.flag, approve=True)
    logger.success(f"accepted friend add request from onebot:{event.user_id}")
