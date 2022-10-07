from .config import conf

if conf.accept_friend_add_request:
    from . import accept_friend_add_request

if conf.accept_group_add_request:
    from . import accept_group_add_request

if conf.accept_group_invite_request:
    from . import accept_group_invite_request
