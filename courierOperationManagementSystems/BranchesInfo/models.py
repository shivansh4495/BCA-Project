from django.db import models

# Create your models here.
class Branches(models.Model):
    Branch_CD = models.IntegerField(primary_key=True)
    Branch_NM = models.CharField(max_length=50, null=False)
    countryId = models.IntegerField(null=False)
    stateId  = models.IntegerField(null=False)
    cityId = models.IntegerField(null=False)
    Address = models.CharField(max_length=100, null=False)

class PacketAssignmentDetails(models.Model):
    Delivery_Boy_Id = models.CharField(max_length=10, null=False)
    AWBNO = models.CharField(max_length=50, null=False)
    Assign_DT = models.DateTimeField(null=False)

class delivery_Boy(models.Model):
    Delivery_Boy_Id = models.BigAutoField(max_length=10, primary_key=True)
    Delivery_Boy_Name = models.CharField(max_length=50, null=False)
    Delivery_Boy_Address = models.CharField(max_length=100, null=False)
    Delivery_Boy_contact_No = models.IntegerField(null=False)
    Delivery_Boy_Area = models.CharField(max_length=30, null=True)
    Branch_CD = models.IntegerField(null=False)

class delivery_Boy_ID(models.Model):
    Current_ID = models.CharField(max_length=4, primary_key=True) 