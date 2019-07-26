from django.db import models

# Create your models here.
class Schedule(models.Model):
	startday = models.CharField(max_length=20, blank=True)
	endday = models.CharField(max_length=20, blank=True)
	starttime =  models.CharField(max_length=10, blank=True)
	endtime =  models.CharField(max_length=10, blank=True)
