from django.shortcuts import render


def home(request):
    context = {"name": "Артем"}
    return render(request, "pages/home.html", context)
