from datetime import date, timedelta

CELL = 26
GAP = 8
STEP = CELL + GAP


def snake_positions(count, columns):
    positions = []
    for index in range(count):
        row = index // columns
        col = index % columns
        if row % 2 == 1:
            col = columns - 1 - col
        positions.append((row, col))
    return positions


def fill_level(amount, daily_target, best_day):
    if amount == 0:
        return 0
    if daily_target:
        share = amount / daily_target
    else:
        share = amount / best_day
    if share >= 1:
        return 3
    if share >= 0.5:
        return 2
    return 1


def build_snake(daily_totals, start, end, daily_target=None, columns=7, until=None):
    last = max(end, until) if until else end
    days_count = (last - start).days + 1
    best_day = max(daily_totals.values(), default=1)
    positions = snake_positions(days_count, columns)

    cells = []
    for index, (row, col) in enumerate(positions):
        day = start + timedelta(days=index)
        is_future = day > end
        amount = 0 if is_future else daily_totals.get(day, 0)
        x = col * STEP
        y = row * STEP
        cells.append(
            {
                "date": day,
                "amount": amount,
                "level": fill_level(amount, daily_target, best_day),
                "x": x,
                "y": y,
                "cx": x + CELL // 2,
                "cy": y + CELL // 2,
                "is_future": is_future,
                "is_today": day == end,
            }
        )

    past = [cell for cell in cells if not cell["is_future"]]
    future = [cell for cell in cells if cell["is_future"]]
    path = " ".join(f"{cell['cx']},{cell['cy']}" for cell in past)
    future_path = ""
    if future:
        future_path = " ".join(
            f"{cell['cx']},{cell['cy']}" for cell in past[-1:] + future
        )

    rows = (days_count + columns - 1) // columns
    return {
        "cells": cells,
        "path": path,
        "future_path": future_path,
        "cell": CELL,
        "width": columns * STEP - GAP,
        "height": rows * STEP - GAP,
    }
    days_count = (end - start).days + 1
    best_day = max(daily_totals.values(), default=1)
    positions = snake_positions(days_count, columns)

    cells = []
    for index, (row, col) in enumerate(positions):
        day = start + timedelta(days=index)
        amount = daily_totals.get(day, 0)
        x = col * STEP
        y = row * STEP
        cells.append(
            {
                "date": day,
                "amount": amount,
                "level": fill_level(amount, daily_target, best_day),
                "x": x,
                "y": y,
                "cx": x + CELL // 2,
                "cy": y + CELL // 2,
            }
        )

    rows = (days_count + columns - 1) // columns
    path = " ".join(f"{cell['cx']},{cell['cy']}" for cell in cells)
    return {
        "cells": cells,
        "path": path,
        "cell": CELL,
        "width": columns * STEP - GAP,
        "height": rows * STEP - GAP,
    }


if __name__ == "__main__":
    start = date(2026, 9, 20)
    end = date(2026, 10, 1)
    totals = {
        date(2026, 9, 20): 30,
        date(2026, 9, 21): 15,
        date(2026, 9, 23): 45,
        date(2026, 9, 24): 30,
        date(2026, 9, 27): 10,
        date(2026, 10, 1): 30,
    }

    snake = build_snake(totals, start, end, daily_target=30, columns=5)

    for cell in snake["cells"]:
        print(
            cell["date"],
            cell["amount"],
            "уровень",
            cell["level"],
            "x",
            cell["x"],
            "y",
            cell["y"],
        )
    print("размер рисунка:", snake["width"], "x", snake["height"])
