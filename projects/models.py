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


class Profile(models.Model):
    full_name = models.CharField("Имя", max_length=200)
    role = models.CharField("Кто я (одна строка)", max_length=300)
    location = models.CharField("Город", max_length=200, blank=True)
    email = models.EmailField("Почта", blank=True)
    telegram = models.CharField("Telegram (без @)", max_length=100, blank=True)
    github = models.CharField("GitHub (логин)", max_length=100, blank=True)
    about = models.TextField("О себе")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиль"

    def __str__(self):
        return self.full_name


class Education(models.Model):
    institution = models.CharField("Учебное заведение", max_length=300)
    details = models.CharField("Уровень, специальность", max_length=300)
    year = models.PositiveIntegerField("Год окончания")

    class Meta:
        ordering = ["-year"]
        verbose_name = "Образование или курс"
        verbose_name_plural = "Образование и курсы"

    def __str__(self):
        return f"{self.institution} ({self.year})"
