# Generated by Django 5.0.7 on 2024-08-03 15:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[("low", "低"), ("medium", "中"), ("high", "高")],
                default="medium",
                max_length=10,
            ),
        ),
    ]
