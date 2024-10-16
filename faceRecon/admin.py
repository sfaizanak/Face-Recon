from django.contrib import admin
from .models import *

class adminData(admin.ModelAdmin):
    list_display = ('username','collegeName')
admin.site.register(collegeAdmin,adminData)

class studentData(admin.ModelAdmin):
    list_display = ('studentName','username','email','collegeName','dept','year','mobile','addr','city')
    
admin.site.register(studentModel,studentData)

class staffData(admin.ModelAdmin):
    list_display = ('staffName','username','email','collegeName','dept','desg','mobile','addr','city')
    
admin.site.register(staffModel,staffData)