# Generated by Django 5.0.3 on 2024-04-22 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("userManagement", "0002_login_info"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="Client_contact_N0",
            new_name="Client_contact_No",
        ),
    ]
