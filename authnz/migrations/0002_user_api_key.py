# Generated by Django 5.0.6 on 2024-06-23 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authnz", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="api_key",
            field=models.CharField(blank=True, default="", max_length=40),
        ),
    ]