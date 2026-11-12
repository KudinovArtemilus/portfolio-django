"""Статистика профиля Stepik через открытый API."""

import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.core.cache import cache

STEPIK_USER_ID = 86215323
API_URL = f"https://stepik.org/api/users/{STEPIK_USER_ID}"
PROFILE_URL = f"https://stepik.org/users/{STEPIK_USER_ID}"

CACHE_KEY = "stepik_stats"
CACHE_OK = 6 * 60 * 60  # удачный ответ храним 6 часов
CACHE_FAIL = 10 * 60  # после ошибки не стучимся 10 минут


def parse(data):
    """Из ответа API берём только то, что покажем на сайте."""
    user = data["users"][0]
    return {
        "solved": user["solved_steps_count"],
        "knowledge": user["knowledge"],
        "url": PROFILE_URL,
    }


def fetch():
    """Сходить в API Stepik. Ждём не больше 3 секунд."""
    request = Request(API_URL, headers={"User-Agent": "portfolio-kudinov"})
    with urlopen(request, timeout=3) as response:
        return parse(json.load(response))


def stepik_stats():
    """Статистика из кэша; если её там нет — из API. При ошибке — None."""
    stats = cache.get(CACHE_KEY)
    if stats is not None:
        return stats or None  # {} в кэше означает «недавно была ошибка»

    try:
        stats = fetch()
    except (URLError, TimeoutError, ValueError, KeyError, IndexError):
        cache.set(CACHE_KEY, {}, CACHE_FAIL)
        return None

    cache.set(CACHE_KEY, stats, CACHE_OK)
    return stats
