# Generated by Django 5.0.3 on 2024-05-01 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BranchesInfo", "0014_delivery_boy_details_delivery_boy_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="data_records",
            name="order_type",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="data_records",
            name="receiver_state",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="data_records",
            name="sender_state",
            field=models.CharField(max_length=30, null=True),
        ),
    ]
