from django.db import models
from django.utils.timezone import now
# Create your models here.

class Event(models.Model):

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Members(models.Model):

    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,default=None)
    email = models.EmailField()
    phone = models.IntegerField()
    reg_type = models.CharField(max_length=100)
    tickets = models.IntegerField()
    photo_id = models.ImageField(upload_to='profile_image',blank=False)
    date = models.DateTimeField(default=now,blank=True)
    reg_number = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.reg_number

