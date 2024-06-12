import uuid 


def generate_unique_code ():
    return uuid.uuid4().hex[:6].upper()