# Generated by Django 4.2.13 on 2024-05-27 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0005_leccion_rename_previas_previa_delete_asistencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profesor',
            name='cursos',
        ),
    ]
