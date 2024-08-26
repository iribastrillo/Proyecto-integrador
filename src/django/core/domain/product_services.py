from domain.models import Curso, Grupo
from profiles.models import Profesor

from core.domain.exceptions import TeacherHasGroupsException, NoAlternativeException

from django.db.models import Q


def products_get_acives():
    return Curso.objects.filter(activo=True, fecha_baja=None)


def group_remove_teacher(teacher: Profesor):
    if teacher.grupo_set.all().count() > 0:
        raise TeacherHasGroupsException()


def group_get_by_product_name(course: Curso):
    return Grupo.objects.filter(curso__nombre=course.nombre)


def group_get_change_alternatives(group: Grupo):
    alts = Grupo.objects.filter(Q(curso__nombre=group.curso.nombre), ~Q(id=group.id))
    if alts.count() == 0:
        raise NoAlternativeException()
    return alts


def group_get_by_id(id: int):
    return Grupo.objects.get(id=id)
