from datetime import datetime, timedelta


def get_expire_time() -> int:
    now: datetime = datetime.now()
    drop_time: datetime = now.replace(hour=14, minute=11, second=0)
    if now > drop_time:
        drop_time += timedelta(days=1)
    res: float = abs((now - drop_time).total_seconds())
    return int(res)
