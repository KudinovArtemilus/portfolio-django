from django.contrib import admin

from .models import Certificate, Education, Experience, Profile, SkillGroup


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["position", "company", "start", "end", "area"]
    list_editable = ["area"]


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["institution", "year"]
    inlines = [CertificateInline]
