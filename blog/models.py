from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Адрес в URL", unique=True)
    summary = models.CharField("Кратко", max_length=300)
    body = models.TextField("Текст (Markdown)")
    is_published = models.BooleanField("Опубликована", default=False)
    published_at = models.DateField("Дата публикации", default=timezone.now)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title
