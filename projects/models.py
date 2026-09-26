from django.db import models


class Project(models.Model):
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Адрес в URL", unique=True)
    summary = models.CharField("Кратко", max_length=300)
    description = models.TextField("Подробное описание")
    stack = models.CharField("Стек", max_length=200)
    github_url = models.URLField("Ссылка на GitHub", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.title
