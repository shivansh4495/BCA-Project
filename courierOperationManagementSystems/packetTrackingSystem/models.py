from django.db import models
# from BranchesInfo.models import delivery_Boy_details

# Create your models here.
class User_Info(models.Model):
    id = models.BigAutoField(primary_key=True)
    User_Id = models.CharField(max_length=30, null=False)
    User_Name = models.CharField(max_length=100, null=False)
    User_Address = models.CharField(max_length=200, null=False)
    User_contact_No = models.CharField(max_length=15, null=True)
    User_Email_Id = models.CharField(max_length=30, null=True)
    Branch_CD = models.IntegerField(null=True)
    
    def __str__(self):
        return self.User_Name

class POD_Records(models.Model):
    AWBNO = models.CharField(max_length=10) #^ removed primary key aspect from this table.
    Del_Status = models.CharField(max_length=20, null=False) #^ delivery status
    Receiver_Name = models.CharField(max_length=100, null= False)
    Receiver_Contact_No = models.CharField(max_length=15, null= True)
    RTO_Reason = models.CharField(max_length=30, null= True)
    Relation = models.CharField(max_length=50, null= True)
    Attempt_Date = models.DateTimeField(null= True)
    
    def __str__(self):
        return self.AWBNO

class printOption(models.Model):
    Branch_CD = models.IntegerField(null= False)
    CurrentAWB = models.CharField(max_length=10, null= False)
    Setting_CD = models.CharField(max_length=1, null= False)

class Rate_Plane_Details(models.Model):
    Plan_code = models.CharField(max_length=10, null= False)
    Description = models.CharField(max_length=255, null= False)
    
    def __str__(self):
        return self.Plan_code

class Qr_Details(models.Model):
    awbno = models.CharField(max_length=100)
    barcode_image = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Barcode {self.id}'


class Live_Updates(models.Model):
    AWBNO = models.CharField(max_length=50)
    transit_status = models.CharField(max_length=100, default='Not Picked Up From Source.')
    update_location = models.CharField(max_length=100)
    last_update_time = models.DateTimeField(null=False)
    Delivery_Boy_Name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.AWBNO} - {self.transit_status}"
