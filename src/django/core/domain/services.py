import uuid
from decimal import Decimal
from string import ascii_uppercase
from itertools import repeat
from datetime import date
import calendar


IVA = Decimal(1.22)


def generate_unique_code():
    return uuid.uuid4().hex[:6].upper()


def generate_group_label(course_group_count):
    return ascii_uppercase[course_group_count]


def calculate_payment(groups):
    total = 0
    for group in groups:
        if group.alumnos.count() > 0:
            course = group.curso
            total += Decimal(course.payout_ratio) * Decimal(course.costo)
    return total / IVA, total


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
    return (earnings - spending) / IVA


def generate_data_enrolments(products):
    data = []
    for product in products:
        data.append({"x": product.nombre, "y": product.alumnocurso_set.count()})
    return data


def prepare_monthly_addtions_data (query):
    data = {
        "month": list(calendar.month_name)[1:],
        "value": [i for i in repeat(0, 12)]
    }
    for d in query:
        data["value"][d["month"] - 1] = d["count"]
    return data