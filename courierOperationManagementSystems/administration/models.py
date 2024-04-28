from django.db import models

# Create your models here.
class Admin_table(models.Model):
    Admin_Id = models.BigAutoField(primary_key=True)
    Admin_Name = models.CharField(max_length=100, null=False)
    Admin_Password = models.CharField(max_length=20, null=False)
    def __str__(self):
        return self.Admin_Name
