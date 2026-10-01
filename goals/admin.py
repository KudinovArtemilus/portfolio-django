from django.contrib import admin

from .models import Entry, Goal


class EntryInline(admin.TabularInline):
    model = Entry
    extra = 1
    fields = ["date", "amount", "note", "note_is_private"]


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ["title", "kind", "unit", "status", "is_public", "start_date"]
    list_editable = ["status", "is_public"]
    list_filter = ["status", "kind", "is_public"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [EntryInline]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["goal", "date", "amount", "note", "note_is_private"]
    list_filter = ["goal"]
    date_hierarchy = "date"
