from django.shortcuts import render

from goals.stats import ru_plural

from .models import Education, Experience, Profile, SkillGroup


def years_text(months):
    years = months // 12
    return f"{years} {ru_plural(years, ('год', 'года', 'лет'))}"


def about(request):
    profile = Profile.objects.first()
    experiences = list(Experience.objects.all())

    automation = sum(job.months() for job in experiences if job.area == "automation")
    it = sum(job.months() for job in experiences if job.area == "it")
    total = sum(job.months() for job in experiences)

    def fill(text):
        return (
            text.replace("{автоматизация}", years_text(automation))
            .replace("{ит}", years_text(it))
            .replace("{общий}", years_text(total))
        )

    context = {
        "profile": profile,
        "about_text": fill(profile.about) if profile else "",
        "role_text": fill(profile.role) if profile else "",
        "experiences": experiences,
        "skill_groups": SkillGroup.objects.all(),
        "education": Education.objects.all(),
    }
    return render(request, "resume/about.html", context)
