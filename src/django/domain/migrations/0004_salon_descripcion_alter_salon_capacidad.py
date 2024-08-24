# Generated by Django 4.2.13 on 2024-05-30 00:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0003_remove_bloquedeclase_duracion_remove_carrera_costo_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="salon",
            name="descripcion",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="salon",
            name="capacidad",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
