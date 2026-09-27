from django.contrib import admin

from .models import Experience, SkillGroup


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["position", "company", "start", "end"]


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
