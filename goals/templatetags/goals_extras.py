from django import template

from ..models import Goal
from ..stats import ru_plural

register = template.Library()

DAY_FORMS = ("день", "дня", "дней")


@register.filter
def unit_word(number, unit):
    return ru_plural(number, Goal.UNIT_FORMS[unit])


@register.filter
def days_word(number):
    return ru_plural(number, DAY_FORMS)
