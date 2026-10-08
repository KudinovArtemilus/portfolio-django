from django.db import models
from django.utils import timezone


class Goal(models.Model):
    KIND_CHOICES = [
        ("book", "Книга"),
        ("course", "Видеокурс"),
        ("series", "Сериал"),
        ("practice", "Практика"),
        ("habit", "Привычка"),
    ]
    UNIT_CHOICES = [
        ("pages", "страницы"),
        ("lessons", "уроки"),
        ("episodes", "серии"),
        ("minutes", "минуты"),
        ("tasks", "задачи"),
    ]
    UNIT_FORMS = {
        "pages": ("страница", "страницы", "страниц"),
        "lessons": ("урок", "урока", "уроков"),
        "episodes": ("серия", "серии", "серий"),
        "minutes": ("минута", "минуты", "минут"),
        "tasks": ("задача", "задачи", "задач"),
    }
    STATUS_CHOICES = [
        ("active", "В процессе"),
        ("done", "Выполнена"),
        ("paused", "На паузе"),
        ("dropped", "Брошена"),
    ]

    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Адрес в URL", unique=True)
    kind = models.CharField("Тип", max_length=20, choices=KIND_CHOICES)
    unit = models.CharField("Единица", max_length=20, choices=UNIT_CHOICES)
    target_amount = models.PositiveIntegerField("Объём", null=True, blank=True)
    initial_amount = models.PositiveIntegerField("Сделано до начала", default=0)
    daily_target = models.PositiveIntegerField("Норма в день", null=True, blank=True)
    start_date = models.DateField("Дата начала", default=timezone.localdate)
    deadline = models.DateField("Срок", null=True, blank=True)
    finished_at = models.DateField("Дата завершения", null=True, blank=True)
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="active"
    )
    is_public = models.BooleanField("Показывать на сайте", default=False)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        ordering = ["status", "-start_date"]
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == "done" and not self.finished_at:
            self.finished_at = timezone.localdate()
        super().save(*args, **kwargs)

    def duration_days(self):
        if not self.finished_at:
            return None
        return (self.finished_at - self.start_date).days + 1


class Entry(models.Model):
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name="Цель",
    )
    date = models.DateField("Дата", default=timezone.localdate)
    amount = models.PositiveIntegerField("Сколько")
    note = models.CharField("Заметка", max_length=300, blank=True)
    note_is_private = models.BooleanField("Личная заметка", default=False)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Отметка"
        verbose_name_plural = "Отметки"

    def __str__(self):
        return f"{self.goal} — {self.date}: {self.amount}"
