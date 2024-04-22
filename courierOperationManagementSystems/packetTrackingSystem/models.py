from django.db import models

# Create your models here.
class User_Info(models.Model):
    User_Id = models.BigAutoField(max_length=50, primary_key=True)
    User_Name = models.CharField(max_length=100, null=False)
    User_Address = models.CharField(max_length=200, null=False)
    User_contact_N0 = models.CharField(max_length=15, null=True)
    User_Email_Id = models.CharField(max_length=30, null=True)
    Branch_CD = models.IntegerField()

class POD_Records(models.Model):
    AWBNO = models.CharField(max_length=10, primary_key=True)
    Del_Status = models.CharField(max_length=20, null=False)
    Receiver_Name = models.CharField(max_length=100, null= False)
    Receiver_Contact_No = models.CharField(max_length=15, null= True)
    RTO_Reason = models.CharField(max_length=30, null= True)
    Relation = models.CharField(max_length=50, null= True)
    Attempt_Date = models.DateTimeField(null= True)

class printOption(models.Model):
    Branch_CD = models.IntegerField(null= False)
    CurrentAWB = models.CharField(max_length=10, null= False)
    Setting_CD = models.CharField(max_length=1, null= False)

class Rate_Plane_Details(models.Model):
    Plan_code = models.CharField(max_length=10, null= False)
    Description = models.CharField(max_length=255, null= False)
