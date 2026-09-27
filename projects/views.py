from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    query = request.GET.get("q", "")
    projects = Project.objects.filter(is_published=True)

    if query:
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(stack__icontains=query)
        )

    context = {"projects": projects, "query": query}

    is_htmx = request.headers.get("HX-Request") and not request.headers.get(
        "HX-Boosted"
    )
    if is_htmx:
        return render(request, "projects/_cards.html", context)
    return render(request, "projects/list.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(request, "projects/detail.html", {"project": project})
