# Generated by Django 4.2.13 on 2024-07-06 20:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0018_alter_grupo_cupo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grupo",
            name="cupo",
            field=models.IntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(
                        1, "La cantidad de alumnos debe estar entre 1 y 50"
                    ),
                    django.core.validators.MaxValueValidator(
                        50, "La cantidad de alumnos debe estar entre 1 y 50"
                    ),
                ],
            ),
        ),
    ]
