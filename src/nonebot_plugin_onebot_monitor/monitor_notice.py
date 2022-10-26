from nonebot import on_notice, logger
from nonebot.adapters.onebot.v11 import NoticeEvent

from nonebot_plugin_onebot_monitor.config import conf
from nonebot_plugin_onebot_monitor.models import data_source
from nonebot_plugin_onebot_monitor.models.notice import NoticeOrm


def parse_notice(event: NoticeEvent) -> NoticeOrm:
    event_dict = event.dict()

    del event_dict["post_type"]

    ntc = NoticeOrm()
    for col_name in NoticeOrm.__dict__:
        if col_name in event_dict:
            setattr(ntc, col_name, event_dict[col_name])
            del event_dict[col_name]
    ntc.extra = event_dict

    return ntc


monitor_notice_matcher = on_notice(priority=1)


@monitor_notice_matcher.handle()
async def monitor_notice(event: NoticeEvent):
    if event.get_event_name() in conf.onebot_monitor_ignore:
        return

    session = data_source.session()
    notice = parse_notice(event)
    session.add(notice)
    logger.debug(f"recorded notice {notice}")
    await session.commit()
