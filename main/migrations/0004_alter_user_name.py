# Generated by Django 5.1.5 on 2025-01-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_user_groups_user_user_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
