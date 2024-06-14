import uuid 
from decimal import Decimal
from string import ascii_uppercase

def generate_unique_code ():
    return uuid.uuid4().hex[:6].upper()

def generate_group_label (course_group_count):
    return ascii_uppercase[course_group_count]

def calculate_payment (groups):
    total = 0
    for group in groups:
        course = group.curso
        total += Decimal(course.payout_ratio) * Decimal(course.costo)
    return total/Decimal('1.22'), total