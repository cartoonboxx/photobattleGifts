def decline_participant(word: str, count: int) -> str:
    if word == 'победител':
        if count % 10 == 1 and count % 100 != 11:
            return f"{word}ь"
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return f"{word}я"
        else:
            return f"{word}ей"
    elif word == 'участник':
        if count % 10 == 1 and count % 100 != 11:
            return f"{word}"
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return f"{word}а"
        else:
            return f"{word}ов"

    return ''