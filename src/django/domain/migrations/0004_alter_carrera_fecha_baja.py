# Generated by Django 4.2.13 on 2024-05-29 22:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0003_remove_bloquedeclase_duracion_remove_carrera_costo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carrera",
            name="fecha_baja",
            field=models.DateField(blank=True, null=True),
        ),
    ]
