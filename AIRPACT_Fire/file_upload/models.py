from __future__ import unicode_literals
from user_profile.models import AirpactUser
from django.db import models

# Create your models here.
class picture(models.Model):
	pic = models.ImageField(upload_to = 'pictures/')
	uploaded = models.DateTimeField(auto_now_add = True)
	description = models.TextField(default = "")
	user = models.ForeignKey(AirpactUser, on_delete=models.CASCADE)
	vr = models.FloatField(null=False, default=0)
	highColor = models.IntegerField(null=False , default=0)
	highX = models.IntegerField(null=False, default=0)
	highY= models.IntegerField(null=False, default=0)
	lowColor = models.IntegerField(null=False, default=0)
	geoX = models.IntegerField(default = 0)
	geoY = models.IntegerField(default = 0)

	def __str__(self):
		return self.description

class tag(models.Model):
	picture = models.ForeignKey(picture, on_delete=models.CASCADE)
	text = models.TextField(null=False)