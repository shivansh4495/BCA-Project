# Generated by Django 5.0.3 on 2024-04-28 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "BranchesInfo",
            "0010_alter_branches_cityid_alter_branches_countryid_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Branch_head",
            fields=[
                (
                    "Branch_head_Id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("Branch_head_Name", models.CharField(max_length=50, null=True)),
                ("Branch_head_Username", models.CharField(max_length=50)),
                ("Branch_head_Password", models.CharField(max_length=50)),
                ("Branch_CD", models.IntegerField(null=True)),
            ],
        ),
    ]
