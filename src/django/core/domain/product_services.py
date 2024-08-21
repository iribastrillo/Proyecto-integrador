from domain.models import Curso
from profiles.models import Profesor

from core.domain.exceptions import TeacherHasGroupsException


def products_get_acives ():
    return Curso.objects.filter (activo=True, fecha_baja=None)


def group_remove_teacher(teacher: Profesor):
    if teacher.grupo_set.all().count() > 0:
        raise TeacherHasGroupsException()