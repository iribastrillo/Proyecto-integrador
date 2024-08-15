from django.db.models.signals import pre_save,post_save, pre_delete,post_delete
from .models import BloqueDeClase,Grupo
from django.dispatch import receiver

def update_grupo_identifier_on_bloque_save(sender, instance, **kwargs):
    print(f"Updating grupo identifier on bloque save: sender {sender}\n instance {instance}\n kwars {kwargs}")
    print(type(instance.grupo))
    id=instance.grupo.id
    grupo = Grupo.objects.get(id=id)
    if grupo:
        grupo.generate_identificador



post_delete.connect(update_grupo_identifier_on_bloque_save, sender=BloqueDeClase)
post_save.connect(update_grupo_identifier_on_bloque_save, sender=BloqueDeClase)

