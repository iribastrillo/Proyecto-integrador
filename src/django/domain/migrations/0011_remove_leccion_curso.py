# Generated by Django 4.2.13 on 2024-06-04 23:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0010_curso_payout_ratio_curso_slug_leccion_curso_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leccion",
            name="curso",
        ),
    ]
