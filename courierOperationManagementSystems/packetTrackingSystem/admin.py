from django.contrib import admin
from . models import User_Info, POD_Records, printOption, Rate_Plane_Details, Live_Updates
# Register your models here.
admin.site.register(User_Info)
admin.site.register(POD_Records)
admin.site.register(printOption)
admin.site.register(Rate_Plane_Details)

admin.site.register(Live_Updates)