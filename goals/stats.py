import math
from datetime import date, timedelta


def is_counted(amount, daily_target):
    if daily_target:
        return amount >= daily_target
    return amount > 0


def current_streak(daily_totals, today, daily_target=None):
    day = today
    if not is_counted(daily_totals.get(day, 0), daily_target):
        day = today - timedelta(days=1)

    streak = 0
    while is_counted(daily_totals.get(day, 0), daily_target):
        streak += 1
        day -= timedelta(days=1)
    return streak


def best_streak(daily_totals, daily_target=None):
    counted_days = sorted(
        day for day, amount in daily_totals.items() if is_counted(amount, daily_target)
    )

    best = 0
    current = 0
    previous = None
    for day in counted_days:
        if previous and day - previous == timedelta(days=1):
            current += 1
        else:
            current = 1
        best = max(best, current)
        previous = day
    return best


def forecast_date(done, target, pace, today):
    remaining = target - done
    if remaining <= 0:
        return today
    if pace <= 0:
        return None
    days_needed = math.ceil(remaining / pace)
    return today + timedelta(days=days_needed)


def required_pace(done, target, deadline, today):
    remaining = target - done
    days_left = (deadline - today).days + 1
    if remaining <= 0 or days_left <= 0:
        return None
    return math.ceil(remaining / days_left)


def average_pace(done, start, today):
    days = max((today - start).days + 1, 1)
    return done / days


def ru_plural(number, forms):
    one, few, many = forms
    number = abs(int(number))
    last_two = number % 100
    last = number % 10
    if 11 <= last_two <= 14:
        return many
    if last == 1:
        return one
    if 2 <= last <= 4:
        return few
    return many


if __name__ == "__main__":
    today = date(2026, 10, 10)
    start = date(2026, 10, 1)
    done = 215
    target = 876
    deadline = date(2026, 11, 30)

    pace = average_pace(done, start, today)
    print("Темп:", round(pace, 1), "стр. в день")
    print("Прогноз окончания:", forecast_date(done, target, pace, today))
    print(
        "Нужный темп к сроку:",
        required_pace(done, target, deadline, today),
        "стр. в день",
    )
