from datetime import datetime
from zoneinfo import ZoneInfo


BEIJING_TZ = ZoneInfo("Asia/Shanghai")


def beijing_now() -> datetime:
    return datetime.now(BEIJING_TZ)