from django.shortcuts import render

from resume.models import Profile


def home(request):
    context = {"profile": Profile.objects.first()}
    return render(request, "pages/home.html", context)
