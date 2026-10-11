import time

from django.shortcuts import render

from .dashboard import build


def page(request):
    context = build(time.time())
    return render(request, "demo/page.html", context)


def live(request):
    context = build(time.time())
    context["oob"] = True
    return render(request, "demo/_live.html", context)
