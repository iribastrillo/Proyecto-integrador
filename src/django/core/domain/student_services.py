from domain.models import Grupo, Alumno
from domain.models import AlumnoCurso as Enrolments
from datetime import date


def students_get_active ():  
    return Enrolments.objects.filter (fecha_baja=None)


def students_get_inactive ():  
    return Enrolments.objects.exclude (fecha_baja=None)


def student_resign_course (student : Alumno, group : Grupo):
    group.alumnos.remove (student)
    enrolment = Enrolments.objects.filter (alumno=student, curso=group.curso, fecha_baja=None).first()
    enrolment.fecha_baja = date.today()
    enrolment.save()
    group.save()
    
    
def student_get_groups (student : Alumno):
    return student.grupo_set.all()


def student_get_by_slug (student_slug : str) -> Alumno:
    return Alumno.objects.get (slug=student_slug)


def student_get_active_enrolments(student : Alumno):
    return Enrolments.objects.filter(alumno=student, fecha_baja=None)