# Generated by Django 5.0.3 on 2024-04-21 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("BranchesInfo", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="packetassignmentdetails",
            old_name="Delievery_Boy_Id",
            new_name="Delivery_Boy_Id",
        ),
    ]
