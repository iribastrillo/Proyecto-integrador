# Generated by Django 4.2.13 on 2024-07-21 16:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0027_alter_dia_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dia",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
