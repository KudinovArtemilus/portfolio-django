from django.shortcuts import render

from .models import Experience, SkillGroup


def about(request):
    context = {
        "experiences": Experience.objects.all(),
        "skill_groups": SkillGroup.objects.all(),
    }
    return render(request, "resume/about.html", context)
