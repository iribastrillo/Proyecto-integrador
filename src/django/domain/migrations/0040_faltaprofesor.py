# Generated by Django 4.2.13 on 2024-08-06 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0010_alumno_sexo_profesor_sexo"),
        ("domain", "0039_alter_pago_options_alter_grupo_fecha_inicio"),
    ]

    operations = [
        migrations.CreateModel(
            name="FaltaProfesor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateTimeField()),
                (
                    "descripcion",
                    models.TextField(blank=True, max_length=250, null=True),
                ),
                (
                    "Grupo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="domain.grupo"
                    ),
                ),
                (
                    "profesor_faltante",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profesor",
                    ),
                ),
                (
                    "profesor_suplente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="substituto",
                        to="profiles.profesor",
                    ),
                ),
            ],
            options={
                "ordering": ["-fecha"],
            },
        ),
    ]
