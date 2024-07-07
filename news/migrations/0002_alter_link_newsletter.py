# Generated by Django 5.0.6 on 2024-07-06 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="newsletter",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="news.newsletter",
            ),
        ),
    ]