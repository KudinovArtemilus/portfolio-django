from datetime import timedelta

from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Goal
from .snake import build_snake
from .stats import (
    average_pace,
    best_streak,
    current_streak,
    forecast_date,
    required_pace,
)

SNAKE_DAYS = 84


def visible_goals(request):
    goals = Goal.objects.exclude(status="dropped")
    if not request.user.is_staff:
        goals = goals.filter(is_public=True)
    return goals


def goal_list(request):
    goals = visible_goals(request).annotate(
        done=Coalesce(Sum("entries__amount"), 0) + F("initial_amount")
    )
    context = {
        "goals": goals.exclude(status="done"),
        "finished": goals.filter(status="done").order_by("-finished_at"),
    }
    return render(request, "goals/list.html", context)


def goal_detail(request, slug):
    goal = get_object_or_404(visible_goals(request), slug=slug)

    rows = goal.entries.values("date").annotate(total=Sum("amount"))
    daily_totals = {row["date"]: row["total"] for row in rows}
    today = timezone.localdate()

    done_since_start = sum(daily_totals.values())
    done = goal.initial_amount + done_since_start
    pace = average_pace(done_since_start, goal.start_date, today)

    stats = {
        "current_streak": current_streak(daily_totals, today, goal.daily_target),
        "best_streak": best_streak(daily_totals, goal.daily_target),
        "pace": round(pace, 1),
    }

    if goal.target_amount and goal.status == "active":
        stats["forecast"] = forecast_date(done, goal.target_amount, pace, today)
        if goal.deadline:
            stats["required"] = required_pace(
                done, goal.target_amount, goal.deadline, today
            )
            stats["on_track"] = (
                stats["forecast"] is not None and stats["forecast"] <= goal.deadline
            )

    start = max(goal.start_date, today - timedelta(days=SNAKE_DAYS - 1))
    limit = today + timedelta(days=SNAKE_DAYS)
    until = None
    if goal.status == "active":
        if goal.deadline:
            until = min(goal.deadline, limit)
        elif stats.get("forecast"):
            until = min(stats["forecast"], limit)
        else:
            until = start + timedelta(days=SNAKE_DAYS - 1)
    snake = build_snake(daily_totals, start, today, goal.daily_target, until=until)

    context = {
        "goal": goal,
        "snake": snake,
        "done": done,
        "stats": stats,
        "entries": goal.entries.all()[:10],
    }
    return render(request, "goals/detail.html", context)
