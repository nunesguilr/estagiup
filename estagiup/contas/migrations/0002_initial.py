# Generated by Django 5.2.3 on 2025-06-20 03:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contas", "0001_initial"),
        ("cursos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aluno",
            name="curso",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cursos.curso",
            ),
        ),
    ]
