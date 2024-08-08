# Generated by Django 4.2.13 on 2024-08-07 17:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0038_merge_20240806_1925"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pago",
            options={"ordering": ["-fecha"]},
        ),
        migrations.AlterField(
            model_name="grupo",
            name="fecha_inicio",
            field=models.DateTimeField(default=datetime.date(2024, 8, 7)),
        ),
    ]