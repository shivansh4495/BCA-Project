# Generated by Django 5.0.3 on 2024-05-06 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("packetTrackingSystem", "0011_live_updates_delete_order_updates"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Qr_Details",
        ),
    ]
