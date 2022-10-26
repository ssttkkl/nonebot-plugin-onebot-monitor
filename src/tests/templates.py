import time

SELF_ID = 123456
USER_ID = 114514
GROUP_ID = 1919810
FLAG = "flagggg"

FORWARD_TO = 1111100000
MESSAGE_ID = 654432
MESSAGE_ID_2 = MESSAGE_ID + 1
MESSAGE_ID_3 = MESSAGE_ID + 2


def friend_request_event():
    from nonebot.adapters.onebot.v11 import FriendRequestEvent
    return FriendRequestEvent(
        time=time.time(), self_id=SELF_ID, post_type="request",
        request_type="friend", user_id=USER_ID, comment="", flag=FLAG
    )


def group_request_event():
    from nonebot.adapters.onebot.v11 import GroupRequestEvent
    return GroupRequestEvent(
        time=time.time(), self_id=SELF_ID, post_type="request",
        request_type="group", sub_type="invite", user_id=USER_ID, group_id=GROUP_ID,
        comment="", flag=FLAG
    )


def private_message_event(message):
    from nonebot.adapters.onebot.v11 import PrivateMessageEvent
    from nonebot.adapters.onebot.v11.event import Sender

    message_event = PrivateMessageEvent(
        time=time.time(), self_id=SELF_ID, post_type="message",
        message_type="private", sub_type="friend", message_id=MESSAGE_ID_2,
        user_id=FORWARD_TO, message=message,
        raw_message=str(message), font=14, sender=Sender()
    )
    return message_event


def group_admin_notice_event():
    from nonebot.adapters.onebot.v11 import GroupAdminNoticeEvent

    return GroupAdminNoticeEvent(
        time=time.time(), self_id=SELF_ID, post_type="notice",
        notice_type="group_admin", sub_type="set", group_id=GROUP_ID,
        user_id=SELF_ID
    )
