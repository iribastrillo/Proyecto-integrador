# Generated by Django 4.2.13 on 2024-06-21 21:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0021_alumnoexamen"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="alumnoexamen",
            options={"verbose_name_plural": "Fallos"},
        ),
        migrations.AlterModelOptions(
            name="examen",
            options={"verbose_name_plural": "Exámenes"},
        ),
        migrations.AlterModelOptions(
            name="leccion",
            options={"verbose_name_plural": "Lecciones"},
        ),
    ]
