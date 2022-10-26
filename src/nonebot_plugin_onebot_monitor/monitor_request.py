from nonebot import on_request, logger
from nonebot.adapters.onebot.v11 import RequestEvent

from nonebot_plugin_onebot_monitor.config import conf
from nonebot_plugin_onebot_monitor.models import data_source
from nonebot_plugin_onebot_monitor.models.request import RequestOrm


def parse_request(event: RequestEvent) -> RequestOrm:
    event_dict = event.dict()

    del event_dict["post_type"]

    ntc = RequestOrm()
    for col_name in RequestOrm.__dict__:
        if col_name in event_dict:
            setattr(ntc, col_name, event_dict[col_name])
            del event_dict[col_name]
    ntc.extra = event_dict

    return ntc


monitor_request_matcher = on_request(priority=1)


@monitor_request_matcher.handle()
async def monitor_request(event: RequestEvent):
    if event.get_event_name() in conf.onebot_monitor_ignore:
        return

    session = data_source.session()
    request = parse_request(event)
    session.add(request)
    logger.debug(f"recorded request {request}")
    await session.commit()
