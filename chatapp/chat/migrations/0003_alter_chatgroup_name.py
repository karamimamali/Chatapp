# Generated by Django 5.0 on 2024-02-06 20:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_chatgroup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatgroup",
            name="name",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]