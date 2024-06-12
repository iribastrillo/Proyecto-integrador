import uuid 
from string import ascii_uppercase

def generate_unique_code ():
    return uuid.uuid4().hex[:6].upper()

def generate_group_label (course_group_count):
    return ascii_uppercase[course_group_count]