# Generated by Django 4.2.13 on 2024-07-28 14:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0029_merge_0025_merge_20240718_1138_0028_alter_dia_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pago",
            name="monto",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[
                    django.core.validators.MinValueValidator(
                        1, "El monto debe ser mayor que cero"
                    ),
                    django.core.validators.MaxValueValidator(
                        1000000, "El monto no debe superar el millón de pesos"
                    ),
                ],
            ),
        ),
    ]
