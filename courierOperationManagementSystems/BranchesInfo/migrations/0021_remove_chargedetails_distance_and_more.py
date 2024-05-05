# Generated by Django 5.0.3 on 2024-05-05 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BranchesInfo", "0020_alter_chargedetails_plancode"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chargedetails",
            name="Distance",
        ),
        migrations.AlterField(
            model_name="chargedetails",
            name="Amount",
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name="chargedetails",
            name="Weight",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
