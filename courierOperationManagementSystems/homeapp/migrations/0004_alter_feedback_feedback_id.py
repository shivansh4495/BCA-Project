# Generated by Django 5.0.3 on 2024-04-22 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homeapp", "0003_delete_login_info"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="Feedback_Id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
