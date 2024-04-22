from django.db import models

# Create your models here.
class Client(models.Model):
    Client_Id = models.CharField(max_length=50, primary_key=True)
    Client_Name = models.CharField(max_length=100, null=False)
    Client_Address = models.CharField(max_length=200, null=False)
    Client_contact_N0 = models.CharField(max_length=15, null=True)
    Client_Email_Id = models.CharField(max_length=30, null=True)

class Login_Info(models.Model):
    User_Id = models.CharField(max_length=50, null=False)
    User_Password = models.CharField(max_length=20, null=False)
    User_Type = models.CharField(max_length=5, null=False)