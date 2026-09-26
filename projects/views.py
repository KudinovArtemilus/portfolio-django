from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, "projects/list.html", {"projects": projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(request, "projects/detail.html", {"project": project})
