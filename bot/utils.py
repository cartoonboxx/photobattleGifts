from urllib.parse import urlparse
from datetime import datetime, timedelta

def normalize_channel_ref(text: str) -> str | None:
    t = text.strip()

    if t.startswith("http://") or t.startswith("https://"):
        parsed = urlparse(t)
        if parsed.netloc.lower() != "t.me":
            return None
        path = parsed.path.lstrip("/")

        if path.startswith("joinchat/") or path.startswith("+"):
            return None

        username = path.split("/", 1)[0]
        username = username.split("?", 1)[0]
        if not username:
            return None
        return f"@{username}"

    if t.lower().startswith("t.me/"):
        username = t.split("/", 1)[1].split("?", 1)[0]
        if not username or username.startswith("+") or username.startswith("joinchat/"):
            return None
        return f"@{username}"

    if t.startswith("@"):
        return t

    return f"@{t}" if t else None

def add_minutes(minutes: int) -> datetime:
    now = datetime.now()
    new_time = now + timedelta(minutes=minutes)
    return new_time

def return_end_time_string(minutes: int) -> str:
    return add_minutes(minutes).strftime("%H:%M")

def return_end_time_string_with_time(time: datetime, minutes: int):
    new_time = time + timedelta(minutes=minutes)
    return new_time

def get_time_until_event(start_time: datetime, minutes: int) -> dict:
    event_time = return_end_time_string_with_time(start_time, minutes)

    current_time = datetime.now()
    time_difference = event_time - current_time

    if time_difference.total_seconds() < 0:
        return {"minutes": 0, "seconds": 0}

    remaining_minutes = time_difference.seconds // 60
    remaining_seconds = time_difference.seconds % 60

    return {"minutes": remaining_minutes, "seconds": remaining_seconds}
