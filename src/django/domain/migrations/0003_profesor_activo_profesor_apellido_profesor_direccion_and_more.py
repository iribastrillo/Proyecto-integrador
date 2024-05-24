# Generated by Django 4.2.13 on 2024-05-22 23:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_alumnocurso_salon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesor',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='apellido',
            field=models.CharField(default='Fabra', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='direccion',
            field=models.CharField(default='Test 1236', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='dni',
            field=models.CharField(default='2165112', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='email',
            field=models.EmailField(default='test@test.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='fecha_alta',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='fecha_baja',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='fecha_nacimiento',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='nombre',
            field=models.CharField(default='test', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='telefono',
            field=models.CharField(default='5553345', max_length=20),
            preserve_default=False,
        ),
    ]