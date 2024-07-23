# Generated by Django 4.2.13 on 2024-07-21 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0026_alter_dia_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dia',
            name='name',
            field=models.CharField(choices=[('LUN', 'Lunes'), ('MAR', 'Martes'), ('MIE', 'Miércoles'), ('JUE', 'Jueves'), ('VIE', 'Viernes'), ('SAB', 'Sábado'), ('DOM', 'Domingo')], max_length=3),
        ),
    ]