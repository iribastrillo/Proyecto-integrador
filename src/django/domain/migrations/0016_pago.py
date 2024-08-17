# Generated by Django 4.2.13 on 2024-06-15 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0007_alter_alumno_slug_alter_profesor_slug"),
        ("domain", "0015_grupo_identificador"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pago",
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
                ("monto", models.DecimalField(decimal_places=2, max_digits=10)),
                ("fecha", models.DateTimeField(auto_now_add=True)),
                (
                    "descripcion",
                    models.TextField(blank=True, max_length=250, null=True),
                ),
                (
                    "comprobante",
                    models.ImageField(blank=True, null=True, upload_to="pagos"),
                ),
                (
                    "alumno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.alumno",
                    ),
                ),
            ],
        ),
    ]
