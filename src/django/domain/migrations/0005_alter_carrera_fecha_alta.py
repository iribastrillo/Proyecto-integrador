# Generated by Django 4.2.13 on 2024-05-29 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0004_alter_carrera_fecha_baja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='fecha_alta',
            field=models.DateField(auto_now_add=True),
        ),
    ]