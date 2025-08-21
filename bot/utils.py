from urllib.parse import urlparse

def normalize_channel_ref(text: str) -> str | None:
    t = text.strip()

    # 1) URL?
    if t.startswith("http://") or t.startswith("https://"):
        parsed = urlparse(t)
        if parsed.netloc.lower() != "t.me":
            return None
        path = parsed.path.lstrip("/")

        # приватные инвайты: t.me/joinchat/... или t.me/+AbCd...
        if path.startswith("joinchat/") or path.startswith("+"):
            return None

        username = path.split("/", 1)[0]
        username = username.split("?", 1)[0]
        if not username:
            return None
        return f"@{username}"

    # 2) короткий t.me/...
    if t.lower().startswith("t.me/"):
        username = t.split("/", 1)[1].split("?", 1)[0]
        if not username or username.startswith("+") or username.startswith("joinchat/"):
            return None
        return f"@{username}"

    # 3) уже @username
    if t.startswith("@"):
        return t

    # 4) просто username
    return f"@{t}" if t else None