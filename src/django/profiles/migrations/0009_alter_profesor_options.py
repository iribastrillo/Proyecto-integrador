# Generated by Django 4.2.13 on 2024-06-20 16:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0008_remove_alumno_activo_remove_alumno_fecha_alta_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profesor",
            options={
                "permissions": [("is_professor", "Es profesor")],
                "verbose_name_plural": "Profesores",
            },
        ),
    ]
