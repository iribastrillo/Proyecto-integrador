# Generated by Django 4.2.13 on 2024-08-12 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0042_alter_grupo_fecha_inicio"),
    ]

    operations = [
        migrations.AddField(
            model_name="grupo",
            name="identificador",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
