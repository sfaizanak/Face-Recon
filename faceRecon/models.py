from django.db import models
from autoslug import AutoSlugField

class collegeAdmin(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    collegeName = models.CharField(max_length = 100)
    
class studentModel(models.Model):
    studentName = models.CharField(max_length = 50)
    username = models.CharField(max_length = 20,unique=True)
    password = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 254)
    collegeName = models.CharField(max_length = 100)
    dept = models.CharField(max_length = 50)
    year = models.CharField(max_length = 10)
    mobile = models.BigIntegerField()
    addr = models.CharField(max_length = 100)
    city = models.CharField(max_length = 20)
    name_slug = AutoSlugField(populate_from='studentName',unique=True,null=True,default=None)
    img = models.FileField(upload_to='studentImg/', max_length=100)
    img_encoded = models.BinaryField(null=True,unique=True)
    
class staffModel(models.Model):
    staffName = models.CharField(max_length = 100)
    username = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 254)
    collegeName = models.CharField(max_length = 100)
    dept = models.CharField(max_length = 50)
    desg = models.CharField(max_length = 20)
    mobile = models.BigIntegerField()
    addr = models.CharField(max_length = 100)
    city = models.CharField(max_length = 20)
    name_slug = AutoSlugField(populate_from='staffName',unique=True,null=True,default=None)
    img = models.FileField(upload_to='staffImg/', max_length=100)
    img_encoded = models.BinaryField(null=True,unique=True)
    