# Generated by Django 4.2.13 on 2024-05-22 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('duracion_meses', models.IntegerField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='cursos')),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.CharField(max_length=8)),
                ('fecha_nacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('cursos', models.ManyToManyField(to='domain.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('duracion_meses', models.IntegerField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='carreras')),
                ('cursos', models.ManyToManyField(to='domain.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('dni', models.CharField(max_length=8)),
                ('fecha_nacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain.carrera')),
                ('cursos', models.ManyToManyField(to='domain.curso')),
            ],
        ),
    ]
