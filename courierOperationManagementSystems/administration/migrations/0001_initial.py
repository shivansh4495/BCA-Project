# Generated by Django 5.0.3 on 2024-04-28 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Admin_table",
            fields=[
                ("Admin_Id", models.BigAutoField(primary_key=True, serialize=False)),
                ("Admin_Name", models.CharField(max_length=100)),
                ("Admin_Password", models.CharField(max_length=20)),
            ],
        ),
    ]
