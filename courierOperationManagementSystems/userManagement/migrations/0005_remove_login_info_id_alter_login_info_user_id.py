# Generated by Django 5.0.3 on 2024-04-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userManagement", "0004_alter_login_info_user_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="login_info",
            name="id",
        ),
        migrations.AlterField(
            model_name="login_info",
            name="User_Id",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
