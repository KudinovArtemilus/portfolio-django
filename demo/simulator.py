"""Симулятор гидростанции: значение любого датчика в любую секунду.

Ничего не хранится. Значение вычисляется формулой от времени,
поэтому у всех посетителей в одну секунду одинаковые данные,
а историю за 10 минут можно пересчитать за миллисекунды.
"""

import math
import random
from dataclasses import dataclass
from functools import lru_cache
from statistics import mean, stdev

CYCLE = 600  # сценарий поломок повторяется каждые 10 минут


@dataclass(frozen=True)
class Sensor:
    key: str
    name: str
    unit: str
    base: float       # нормальный уровень
    wave: float       # размах медленного колебания
    period: float     # период колебания, секунды
    noise: float      # случайный шум
    fault: str        # какая поломка у этого датчика
    fault_start: int  # секунда цикла, когда поломка начинается
    fault_length: int # сколько секунд длится
    fault_name: str   # как поломка называется для человека
    meaning: str      # что это значит на производстве


SENSORS = [
    Sensor(
        "pressure", "Давление в системе", "бар", 140, 3, 300, 0.8,
        "spike", 120, 15, "Скачок давления",
        "Резкий скачок: гидроудар при переключении клапана или ложный сигнал. "
        "Один раз — не страшно, часто — повод проверить клапаны и сам датчик.",
    ),
    Sensor(
        "current", "Ток двигателя насоса", "А", 38, 1, 240, 0.4,
        "drift", 300, 120, "Рост тока насоса",
        "Ток растёт при той же работе: насосу тяжелее крутиться. Так начинается "
        "износ насоса или засорение фильтра — задолго до остановки линии.",
    ),
    Sensor(
        "axis", "Время хода оси Z", "с", 3.6, 0.05, 420, 0.08,
        "slow", 420, 120, "Замедление оси",
        "Ось ходит медленнее: до цилиндра доходит меньше масла. Причина — "
        "внутренние утечки или упавшая производительность насоса.",
    ),
    Sensor(
        "oil", "Температура масла", "°C", 47, 1.5, 900, 0.2,
        "stuck", 0, 100, "Залипание датчика",
        "Показание застыло, а живой датчик всегда немного «дышит». Скорее всего, "
        "обрыв провода или зависший канал — этим данным сейчас верить нельзя.",
    ),
]


def normal_value(sensor, t):
    """Значение исправного датчика в секунду t."""
    rng = random.Random(f"{sensor.key}:{t}")  # одинаковое число для одной секунды
    wave = sensor.wave * math.sin(2 * math.pi * t / sensor.period)
    return sensor.base + wave + rng.gauss(0, sensor.noise)


def fault_phase(sensor, t):
    """Сколько секунд идёт поломка, или None, если датчик исправен."""
    second = t % CYCLE
    passed = second - sensor.fault_start
    if 0 <= passed < sensor.fault_length:
        return passed
    return None


def value(sensor, t):
    """Значение датчика в секунду t с учётом поломки."""
    t = int(t)
    passed = fault_phase(sensor, t)
    if passed is None:
        return normal_value(sensor, t)

    if sensor.fault == "stuck":     # датчик залип: показывает одно и то же
        return normal_value(sensor, t - passed)
    if sensor.fault == "spike":     # короткий скачок
        return normal_value(sensor, t) + 25
    if sensor.fault == "drift":     # медленный рост, как при износе
        return normal_value(sensor, t) + passed * 0.05
    if sensor.fault == "slow":      # ось стала ходить медленнее
        return normal_value(sensor, t) + 0.6
    return normal_value(sensor, t)


@lru_cache
def reference(sensor, seconds=3600):
    """Эталон: среднее и σ за час заведомо исправной работы.

    Считается один раз и запоминается (lru_cache).
    """
    values = [normal_value(sensor, t) for t in range(seconds)]
    return mean(values), stdev(values)


def history(sensor, now, seconds=600, step=5):
    """Список (время, значение) за последние seconds секунд с шагом step."""
    now = int(now) - int(now) % step
    return [(t, round(value(sensor, t), 2)) for t in range(now - seconds, now + 1, step)]


if __name__ == "__main__":
    import time

    now = int(time.time())
    print("Секунда цикла сейчас:", now % CYCLE)
    for sensor in SENSORS:
        points = history(sensor, now, seconds=60, step=10)
        values = [v for _, v in points]
        status = "ПОЛОМКА" if fault_phase(sensor, now) is not None else "норма"
        print(f"{sensor.name:22} {values[-1]:7.2f} {sensor.unit:4} {status:8} {values}")
