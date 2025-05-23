# Generated by Django 5.0.3 on 2024-05-05 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BranchesInfo", "0025_alter_delivery_boy_details_number_of_alloted_packets"),
        ("packetTrackingSystem", "0008_order_updates_delete_packet"),
    ]

    operations = [
        migrations.AddField(
            model_name="order_updates",
            name="delivery_boy",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="BranchesInfo.delivery_boy_details",
            ),
            preserve_default=False,
        ),
    ]
