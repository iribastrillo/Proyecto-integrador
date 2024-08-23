import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count


def get_weekdays_per_month(day, month):
    year = 2024
    month = 3
    day_to_count = day - 1

    matrix = calendar.monthcalendar(year, month)
    num_days = sum(1 for x in matrix if x[day_to_count] != 0)
    return 1, 1
