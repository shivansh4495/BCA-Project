# Generated by Django 5.0.3 on 2024-04-26 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("packetTrackingSystem", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_info",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
