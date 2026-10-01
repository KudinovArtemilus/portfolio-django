from django.db.models import Sum
from django.shortcuts import render

from .models import Goal


def goal_list(request):
    goals = Goal.objects.exclude(status="dropped").annotate(done=Sum("entries__amount"))

    if not request.user.is_staff:
        goals = goals.filter(is_public=True)

    return render(request, "goals/list.html", {"goals": goals})
