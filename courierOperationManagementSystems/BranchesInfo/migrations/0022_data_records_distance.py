# Generated by Django 5.0.3 on 2024-05-05 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BranchesInfo", "0021_remove_chargedetails_distance_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="data_records",
            name="Distance",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
