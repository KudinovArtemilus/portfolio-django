from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "created_at"]
    list_editable = ["order", "is_published"]
    prepopulated_fields = {"slug": ["title"]}
