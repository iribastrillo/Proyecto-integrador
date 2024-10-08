# Generated by Django 4.2.13 on 2024-06-20 00:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0017_alter_salon_nombre"),
    ]

    operations = [
        migrations.AddField(
            model_name="alumnocarrera",
            name="fecha_baja",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="alumnocurso",
            name="fecha_baja",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="alumnocarrera",
            name="fecha_finalizado",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="alumnocarrera",
            name="fecha_inscripcion",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="alumnocurso",
            name="fecha_finalizado",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="alumnocurso",
            name="fecha_inscripcion",
            field=models.DateField(auto_now_add=True),
        ),
    ]
