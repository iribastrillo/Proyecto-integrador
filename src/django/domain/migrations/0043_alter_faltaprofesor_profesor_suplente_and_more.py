# Generated by Django 4.2.13 on 2024-08-11 00:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_alumno_emergency_contact'),
        ('domain', '0042_merge_20240808_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faltaprofesor',
            name='profesor_suplente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substituto', to='profiles.profesor'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='fecha_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
