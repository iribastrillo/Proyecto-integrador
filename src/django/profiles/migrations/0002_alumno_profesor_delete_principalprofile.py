# Generated by Django 4.2.13 on 2024-05-27 20:22

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0006_remove_profesor_cursos'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.CharField(max_length=8)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, validators=[utils.validators.EmailValidator()])),
                ('fecha_baja', models.DateField(blank=True, null=True)),
                ('fecha_alta', models.DateField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.CharField(max_length=8)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, validators=[utils.validators.EmailValidator()])),
                ('fecha_baja', models.DateField(blank=True, null=True)),
                ('fecha_alta', models.DateField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
                ('cursos', models.ManyToManyField(to='domain.curso')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PrincipalProfile',
        ),
    ]
