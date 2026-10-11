"""Собирает всё, что нужно странице демо, на один момент времени."""

from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings

from .detectors import check
from .simulator import CYCLE, SENSORS, history, reference

STEP = 5          # шаг точек на графике, секунды
CALM = 3          # сколько спокойных проверок подряд нужно, чтобы считать норму восстановленной
WINDOW = 600      # сколько видно на графике: 10 минут
CHART_W = 300
CHART_H = 90


def clock(t):
    """Секунды Unix -> 'ЧЧ:ММ:СС' по времени сайта."""
    tz = ZoneInfo(settings.TIME_ZONE)
    return datetime.fromtimestamp(t, tz=tz).strftime("%H:%M:%S")


def human(text):
    """Десятичная запятая, как принято в русском тексте."""
    return text.replace(".", ",")


def chart(points, norm):
    """Координаты для SVG-графика: линия, коридор нормы, точки вне нормы."""
    m, s = norm
    lower, upper = m - 3 * s, m + 3 * s
    values = [v for _, v in points]
    low = min(min(values), lower)
    high = max(max(values), upper)
    pad = (high - low) * 0.12 or 1
    low, high = low - pad, high + pad

    def x(i):
        return round(i * CHART_W / (len(points) - 1), 1)

    def y(v):
        return round(CHART_H - (v - low) / (high - low) * CHART_H, 1)

    line = " ".join(f"{x(i)},{y(v)}" for i, v in enumerate(values))
    outside = [
        {"x": x(i), "y": y(v)}
        for i, v in enumerate(values)
        if v > upper or v < lower
    ]
    return {
        "line": line,
        "band_y": y(upper),
        "band_h": round(y(lower) - y(upper), 1),
        "outside": outside,
        "last_x": x(len(values) - 1),
        "last_y": y(values[-1]),
        "width": CHART_W,
        "height": CHART_H,
    }


def sensor_state(sensor, now):
    """Текущее значение, проблема, график и события одного датчика."""
    norm = reference(sensor)
    # Берём 20 минут: 10 видно на графике, ещё 10 нужны детекторам как история.
    points = history(sensor, now, seconds=WINDOW * 2, step=STEP)
    values = [v for _, v in points]
    size = WINDOW // STEP + 1

    events = []
    current = None   # проблема, о которой сейчас тревожимся
    calm = 0         # сколько проверок подряд всё спокойно
    for end in range(size, len(values) + 1):
        t = points[end - 1][0]
        problem = check(values[end - size:end], norm)
        if problem:
            calm = 0
            if not current:
                events.append({"t": t, "sensor": sensor, "alarm": True,
                               "title": problem[0], "details": human(problem[1])})
            current = problem
        elif current:
            calm += 1
            if calm >= CALM:  # гистерезис: одной спокойной точки мало
                events.append({"t": t, "sensor": sensor, "alarm": False,
                               "title": "Норма", "details": "показания вернулись в коридор"})
                current = None

    m, s = norm
    return {
        "sensor": sensor,
        "value": values[-1],
        "problem": (current[0], human(current[1])) if current else None,
        "lower": m - 3 * s,
        "upper": m + 3 * s,
        "chart": chart(points[-size:], norm),
        "events": events,
    }


def timeline(now):
    """Сценарий поломок на 10 минут и где мы сейчас."""
    second = now % CYCLE
    segments = [
        {
            "sensor": sensor,
            "left": sensor.fault_start / CYCLE * 100,
            "width": sensor.fault_length / CYCLE * 100,
            "active": sensor.fault_start <= second < sensor.fault_start + sensor.fault_length,
        }
        for sensor in SENSORS
    ]
    upcoming = sorted(
        ((sensor.fault_start - second) % CYCLE, sensor) for sensor in SENSORS
        if not (sensor.fault_start <= second < sensor.fault_start + sensor.fault_length)
    )
    wait, sensor = upcoming[0]
    return {
        "segments": segments,
        "marker": second / CYCLE * 100,
        "next_name": sensor.fault_name,
        "next_in": f"{wait // 60}:{wait % 60:02d}",
    }


def build(now):
    now = int(now)
    sensors = [sensor_state(sensor, now) for sensor in SENSORS]
    events = sorted(
        (event for state in sensors for event in state["events"]),
        key=lambda event: event["t"],
        reverse=True,
    )[:8]
    for event in events:
        event["time"] = clock(event["t"])
    return {
        "sensors": sensors,
        "by_key": {state["sensor"].key: state for state in sensors},
        "events": events,
        "timeline": timeline(now),
        "clock": clock(now),
        "alarms": sum(1 for state in sensors if state["problem"]),
    }
