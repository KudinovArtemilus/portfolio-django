"""Детекторы: по истории значений находят, что с датчиком что-то не так."""

from statistics import mean

RECENT = 6  # последние 6 точек (30 секунд при шаге 5 с) — «сейчас»


def split(values):
    """Делим историю на базу (как было) и недавнее (что сейчас)."""
    return values[:-RECENT], values[-RECENT:]


def out_of_3_sigma(values, norm):
    """Последние 3 точки подряд выходят за эталон: среднее ± 3σ."""
    _, recent = split(values)
    m, s = norm
    upper, lower = m + 3 * s, m - 3 * s
    outside = [v for v in recent[-3:] if v > upper or v < lower]
    if len(outside) == 3:
        return f"вне 3σ: {recent[-1]:.2f} при норме {lower:.2f}…{upper:.2f}"
    return None


def stuck(values, norm, tolerance=1e-6):
    """Значение не меняется — живой датчик всегда немного шумит."""
    _, recent = split(values)
    if max(recent) - min(recent) <= tolerance:
        return f"значение не меняется: {recent[-1]:.2f}"
    return None


def spike(values, norm, factor=6):
    """Резкий скачок между соседними точками, намного больше обычного шага."""
    base, recent = split(values)
    steps = [abs(b - a) for a, b in zip(base, base[1:])]
    if len(steps) < 20:
        return None
    usual = mean(steps)
    jumps = [abs(b - a) for a, b in zip(recent, recent[1:])]
    if max(jumps) > factor * usual:
        return f"скачок на {max(jumps):.2f} при обычном шаге {usual:.2f}"
    return None


DETECTORS = [
    ("Залипание", stuck),
    ("Скачок", spike),
    ("Вне нормы", out_of_3_sigma),
]


def check(values, norm):
    """Первая найденная проблема: (название, подробности) или None.

    norm = (среднее, σ) эталона.
    """
    for title, detector in DETECTORS:
        details = detector(values, norm)
        if details:
            return title, details
    return None


if __name__ == "__main__":
    import time

    from demo.simulator import SENSORS, history, reference

    now = int(time.time())
    for sensor in SENSORS:
        values = [v for _, v in history(sensor, now)]
        problem = check(values, reference(sensor))
        text = " — ".join(problem) if problem else "норма"
        print(f"{sensor.name:22} {values[-1]:7.2f} {sensor.unit:4} {text}")
