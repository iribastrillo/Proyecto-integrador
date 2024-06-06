from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def group_is_not_full (value):
    if value.alumnos.count() >= value.cupo:
        raise ValidationError(
            _("El cupo está lleno."),
        )
        
