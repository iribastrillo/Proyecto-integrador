from decimal import Decimal

from domain.models import Grupo, Alumno, Pago
from domain.models import AlumnoCurso as Enrolments
from datetime import date

from core.domain.exceptions import (
    StudentAlreadyEnroledException,
    GroupCompleteException,
    ProductsDoNotMatchException,
    StudentHasEnroledException,
)


def students_get_active():
    return Enrolments.objects.filter(fecha_baja=None)


def student_get_active_products(student: Alumno):
    return Enrolments.objects.filter(
        alumno=student, fecha_baja=None, fecha_finalizado=None, aprobado=False
    )


def student_get_last_payments(student: Alumno):
    return Pago.objects.filter(alumno=student)[:5]


def students_get_inactive():
    return Enrolments.objects.exclude(fecha_baja=None)


def student_resign_course(student: Alumno, group: Grupo):
    group.alumnos.remove(student)
    enrolment = Enrolments.objects.filter(
        alumno=student, curso=group.curso, fecha_baja=None
    ).first()
    enrolment.fecha_baja = date.today()
    enrolment.save()
    group.save()


def student_enroll(student: Alumno, group: Grupo, fee: Decimal):
    if group.alumnos.filter(slug=student.slug).exists():
        raise StudentAlreadyEnroledException()
    if student.alumnocurso_set.filter(
        curso__nombre=group.curso.nombre, fecha_baja=None
    ).exists():
        raise StudentHasEnroledException()
    if group.actives == group.cupo:
        raise GroupCompleteException()
    group.alumnos.add(student)
    Enrolments.objects.create(alumno=student, curso=group.curso, fee=fee)
    group.save()


def student_change_group(student: Alumno, fr: Grupo, to: Grupo):
    if to.actives == to.cupo:
        raise GroupCompleteException()
    if fr.curso.nombre != to.curso.nombre:
        raise ProductsDoNotMatchException()
    fr.alumnos.remove(student)
    to.alumnos.add(student)
    fr.save()
    to.save()


def student_get_groups(student: Alumno):
    return student.grupo_set.all()


def student_get_by_slug(student_slug: str) -> Alumno:
    return Alumno.objects.get(slug=student_slug)


def student_get_by_user(user_id: str) -> Alumno:
    return Alumno.objects.get(user__id=user_id)


def student_get_active_enrolments(student: Alumno):
    return Enrolments.objects.filter(alumno=student, fecha_baja=None)
