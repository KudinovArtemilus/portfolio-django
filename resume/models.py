from datetime import date

from django.db import models

from goals.stats import ru_plural


def months_between(start, end):
    """Сколько полных месяцев между двумя датами."""
    return (end.year - start.year) * 12 + (end.month - start.month)


def format_duration(months):
    """42 -> '3 года 6 мес.'"""
    years, rest = divmod(months, 12)
    parts = []
    if years:
        parts.append(f"{years} {ru_plural(years, ('год', 'года', 'лет'))}")
    if rest:
        parts.append(f"{rest} мес.")
    return " ".join(parts) or "меньше месяца"


class Experience(models.Model):
    position = models.CharField("Должность", max_length=200)
    company = models.CharField("Компания", max_length=200)
    start = models.DateField("Начало")
    end = models.DateField("Окончание", null=True, blank=True)
    description = models.TextField("Что делал", blank=True)

    AREA_CHOICES = [
        ("automation", "Автоматизация"),
        ("it", "IT"),
        ("other", "Другое"),
    ]
    area = models.CharField(
        "Сфера", max_length=20, choices=AREA_CHOICES, default="other"
    )

    class Meta:
        ordering = ["-start"]
        verbose_name = "Место работы"
        verbose_name_plural = "Опыт работы"

    def __str__(self):
        return f"{self.position} — {self.company}"

    def months(self):
        end = self.end or date.today()
        return months_between(self.start, end)

    def duration(self):
        return format_duration(self.months())


class SkillGroup(models.Model):
    name = models.CharField("Группа", max_length=100)
    skills = models.TextField("Навыки через запятую")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Группа навыков"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name

    def skill_list(self):
        return [s.strip() for s in self.skills.split(",") if s.strip()]


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
