# Generated by Django 4.2.13 on 2024-06-13 00:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0016_alter_salon_capacidad"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salon",
            name="nombre",
            field=models.CharField(
                error_messages={"nombre": "Ya existe un registro con este nombre."},
                max_length=50,
                unique=True,
            ),
        ),
    ]
