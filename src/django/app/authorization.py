from domain.models import Alumno, Profesor


def is_student(user):
    try:
        return Alumno.objects.filter(user=user).exists()
    except Alumno.DoesNotExist:
        return None


def is_teacher(user):
    try:
        return Profesor.objects.filter(user=user).exists()
    except Profesor.DoesNotExist:
        return None


def is_staff(user):
    return user.is_staff
