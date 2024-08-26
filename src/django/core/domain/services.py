import uuid
from decimal import Decimal
from string import ascii_uppercase
from itertools import repeat
from datetime import date
from typing import Union
from django.contrib.auth.models import User
import calendar

from .utils import get_weekdays_per_month


IVA = Decimal(1.22)


def generate_unique_code():
    return uuid.uuid4().hex[:6].upper()


def generate_group_label(course_group_count):
    return ascii_uppercase[course_group_count]


def get_current_month_amount_receivable(enrolments):
    receivable = 0
    for enrolment in enrolments:
        if enrolment.fecha_finalizado == None:
            receivable += enrolment.fee
    return receivable


def get_class_to_salary_ratio(group):
    csr = 1
    today = date.today()
    if group.fecha_inicio.month != today.month:
        pass
    else:
        day = group.fecha_inicio.day
        month = group.fecha_inicio.month
        starting_day = date(today.year, month, day)
        count = get_weekdays_per_month(day, month)
    return csr


def calculate_payment(groups):
    total = 0
    for group in groups:
        if group.alumnos.count() > 0:
            course = group.curso
            total += (
                Decimal(course.payout_ratio)
                * Decimal(course.costo)
                * group.alumnos.count()
            )
    return total / IVA, total


def calculate_actual_fee(enrolments):
    total = 0
    for enrolment in enrolments:
        total += enrolment.fee
    return total


def calculate_total_teacher_spending(professors):
    total = 0
    for professor in professors:
        total += calculate_payment(professor.grupo_set.all())[0]
    return total


def calculate_total_product_earnings(payments):
    total = 0
    for payment in payments.filter(fecha__month=date.today().month):
        total += Decimal(payment.monto)
    return total


def calculate_gains(earnings, spending):
    return earnings - spending


def generate_additions_data(products):
    data = []
    for product in products:
        data.append({"x": product.nombre, "y": product.active_enrolments})
    return data


def generate_dropouts_data(products):
    data = []
    for product in products:
        data.append({"x": product.nombre, "y": product.inactive_enrolments})
    return data


def generate_monthly_addtions_data(query):
    data = {"month": list(calendar.month_name)[1:], "value": [i for i in repeat(0, 12)]}
    for d in query:
        data["value"][d["month"] - 1] = d["count"]
    return data


def generate_monthly_dropouts_data(query):
    data = {"month": list(calendar.month_name)[1:], "value": [i for i in repeat(0, 12)]}
    for d in query:
        data["value"][d["month"] - 1] = d["count"]
    return data
