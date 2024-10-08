# Generated by Django 4.2.13 on 2024-06-05 23:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0013_carrera_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="curso",
            name="payout_ratio",
            field=models.DecimalField(
                decimal_places=2,
                default=0.5,
                max_digits=3,
                validators=[
                    django.core.validators.MaxValueValidator(
                        1, "El valor debe estar entre 1 y 0."
                    ),
                    django.core.validators.MinValueValidator(
                        0, "El valor debe estar entre 1 y 0."
                    ),
                ],
            ),
        ),
    ]
