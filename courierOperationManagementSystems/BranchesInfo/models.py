from django.db import models
import random
import string

# Create your models here.
class Branches(models.Model):
    Branch_CD = models.IntegerField(primary_key=True)
    Branch_NM = models.CharField(max_length=50, null=False) #~ Name of branch
    countryId = models.CharField(max_length=50,null=True) #~ Country code of branch
    stateId  = models.CharField(max_length=50,null=True)
    cityId = models.CharField(max_length=50,null=True)
    Address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    Branch_head =models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"{self.Branch_CD} - {self.Branch_NM}"


class PacketAssignmentDetails(models.Model):
    Delivery_Boy_Id = models.CharField(max_length=10, null=False)
    AWBNO = models.CharField(max_length=50, null=False)
    Assign_DT = models.DateTimeField(null=False)
    def __str__(self):
        return self.Delivery_Boy_Id


class delivery_Boy_details(models.Model):
    Delivery_Boy_Id = models.BigAutoField(primary_key=True)
    Delivery_Boy_Name = models.CharField(max_length=50, null=False)
    Delivery_Boy_Username = models.CharField(max_length=50, null=False)
    Delivery_Boy_Password = models.CharField(max_length=50, null=False)
    Delivery_Boy_Address = models.CharField(max_length=100, null=False)
    Delivery_Boy_contact_No = models.IntegerField(null=False)
    Delivery_Boy_Area = models.CharField(max_length=30, null=True) #! use as branch name 
    Branch_CD = models.IntegerField(null=False)
    User_Type=models.CharField(max_length=20, null=False)

class delivery_Boy_ID(models.Model):
    Current_ID = models.CharField(max_length=4, primary_key=True) 

class ChargeDetails(models.Model):
    PlanCode = models.IntegerField(primary_key=True)
    Distance = models.CharField(max_length=50, null=False)
    Weight = models.CharField(max_length=10, null=False)
    Amount = models.CharField(max_length=10, null=False)
    def __str__(self):
        return self.PlanCode

class CityDetails(models.Model):
    CityId = models.BigAutoField(primary_key=True)
    stateId = models.ImageField(null=False)
    CityName = models.CharField(max_length=50, null=False)

class Data_Records(models.Model):
    AWBNO = models.CharField(max_length=10, primary_key=True)
    Sender_Name = models.CharField(max_length=100, null=True)
    Sender_Address = models.CharField(max_length=100, null=True)
    Sender_Contact_No = models.CharField(max_length=15, null=True)
    Sender_City = models.CharField(max_length=30, null=True)
    Receiver_Name = models.CharField(max_length=100, null=False)
    Receiver_Address = models.CharField(max_length=100, null=True)
    Receiver_Contact_No = models.CharField(max_length=15, null=True)
    Receiver_City = models.CharField(max_length=30, null=True)
    Book_date = models.DateTimeField(null=False)
    Weight = models.CharField(max_length=10, null=True)
    Price = models.CharField(max_length=10, null=True)
    POD_Flag = models.CharField(max_length=20, null=True)
    Print_Flag = models.CharField(max_length=20, null=True)
    Pin_Number = models.CharField(max_length=10, null=True)
    State = models.CharField(max_length=30, null=True)
    Country = models.CharField(max_length=30, null=True)
    Sender_Branch_CD = models.IntegerField()
    Receiver_Branch_CD  = models.IntegerField()
    Type = models.CharField(max_length=50, null=True)
    Client_Id = models.CharField(max_length=50, null=True)
    Alert_Flag = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        if not self.AWBNO:
            # Generate a unique alphanumeric ID
            self.AWBNO = self.generate_unique_awbno()
        super().save(*args, **kwargs)

    def generate_unique_awbno(self):
        # Generate a random alphanumeric string
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        # Combine with a prefix (e.g., 'AWB_') to form the AWBNO
        awbno = 'AWB_' + random_chars
        # Check if the generated AWBNO already exists, generate a new one if it does
        while Data_Records.objects.filter(AWBNO=awbno).exists():
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            awbno = 'AWB_' + random_chars
        return awbno

    def __str__(self):
        return self.AWBNO


class Branch_head(models.Model):
    Branch_head_Id = models.BigAutoField(primary_key=True)
    Branch_head_Name = models.CharField(max_length=50, null=True)
    Branch_head_Username = models.CharField(max_length=50, null=False)
    Branch_head_Password = models.CharField(max_length=50, null=False)
    Branch_CD = models.IntegerField(null=True) 
    User_Type=models.CharField(max_length=20, null=False)

    def __str__(self):
        return f"{self.Branch_head_Id} - {self.Branch_head_Name}"