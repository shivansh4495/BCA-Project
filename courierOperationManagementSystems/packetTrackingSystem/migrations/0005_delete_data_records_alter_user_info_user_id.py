# Generated by Django 5.0.3 on 2024-04-22 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "packetTrackingSystem",
            "0004_rename_reciever_contact_no_pod_records_receiver_contact_no_and_more",
        ),
    ]

    operations = [
        migrations.DeleteModel(
            name="Data_Records",
        ),
        migrations.AlterField(
            model_name="user_info",
            name="User_Id",
            field=models.BigAutoField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
