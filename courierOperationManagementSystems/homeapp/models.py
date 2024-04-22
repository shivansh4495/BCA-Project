from django.db import models

# Create your models here.
class Feedback(models.Model):
    Feedback_Id = models.BigAutoField(primary_key=True)
    Fname = models.CharField(max_length=50, null=False)
    Lname = models.CharField(max_length=50, null=False)
    ContactNo = models.CharField(max_length=50, null=True)
    FeedbackMsg = models.TextField(null=False)
    Date = models.DateTimeField(null= True)
    Email = models.CharField(max_length=100, null=True)
    Reply_flag = models.CharField(max_length=1, null=False)
