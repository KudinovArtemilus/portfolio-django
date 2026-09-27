from django.db import models


class Experience(models.Model):
    position = models.CharField("Должность", max_length=200)
    company = models.CharField("Компания", max_length=200)
    start = models.DateField("Начало")
    end = models.DateField("Окончание", null=True, blank=True)
    description = models.TextField("Что делал", blank=True)

    class Meta:
        ordering = ["-start"]
        verbose_name = "Место работы"
        verbose_name_plural = "Опыт работы"

    def __str__(self):
        return f"{self.position} — {self.company}"


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
