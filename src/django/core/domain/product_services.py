from domain.models import Curso


def products_get_acives ():
    return Curso.objects.filter (activo=True, fecha_baja=None)