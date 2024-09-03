from django.db.models.signals import post_save, post_delete
from .models import BloqueDeClase, Grupo


def update_grupo_identifier_on_bloque_save(sender, instance, **kwargs):
    id = instance.grupo.id
    grupo = Grupo.objects.get(id=id)
    if grupo:
        grupo.generate_identificador


post_delete.connect(update_grupo_identifier_on_bloque_save, sender=BloqueDeClase)
post_save.connect(update_grupo_identifier_on_bloque_save, sender=BloqueDeClase)
