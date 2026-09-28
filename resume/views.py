from django.shortcuts import render

from .models import Education, Experience, Profile, SkillGroup


def about(request):
    context = {
        "profile": Profile.objects.first(),
        "experiences": Experience.objects.all(),
        "skill_groups": SkillGroup.objects.all(),
        "education": Education.objects.all(),
    }
    return render(request, "resume/about.html", context)
