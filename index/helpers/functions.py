from datetime import datetime
from django.core.validators import MaxValueValidator


def current_year():
    return datetime.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)
