from django.db import models

# Create your models here.
class Client(models.Model):
    Client_Id = models.BigAutoField(primary_key=True)
    Client_Name = models.CharField(max_length=100, null=False)
    Client_Address = models.CharField(max_length=200, null=False)
    Client_contact_No = models.CharField(max_length=15, null=True)
    Client_Email_Id = models.CharField(max_length=30, null=True)
    def __str__(self):
        return f"{self.Client_Id} - {self.Client_Name}"


class Login_Info(models.Model):
    User_Id = models.CharField(max_length=50, null=False)
    User_Password = models.CharField(max_length=20, null=False)
    User_Type = models.CharField(max_length=7, null=False)
    def __str__(self):
        return self.User_Id