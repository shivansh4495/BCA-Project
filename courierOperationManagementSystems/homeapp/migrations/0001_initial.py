# Generated by Django 5.0.3 on 2024-04-20 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("Feedback_Id", models.IntegerField(primary_key=True, serialize=False)),
                ("Fname", models.CharField(max_length=50)),
                ("Lname", models.CharField(max_length=50)),
                ("ContactNo", models.CharField(max_length=50, null=True)),
                ("FeedbackMsg", models.TextField()),
                ("Date", models.DateTimeField(null=True)),
                ("Email", models.CharField(max_length=100, null=True)),
                ("Reply_flag", models.CharField(max_length=1)),
            ],
        ),
    ]
