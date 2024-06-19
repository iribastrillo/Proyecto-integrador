import uuid
from decimal import Decimal
from string import ascii_uppercase


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


def calculate_total_product_earnings(enrolments):
    total = 0
    for enrolment in enrolments:
        total += Decimal(enrolment.curso.costo)
    return total


def calculate_gains(earnings, spending):
    return (earnings - spending) / IVA


def get_students_by_product(products):
    pass
