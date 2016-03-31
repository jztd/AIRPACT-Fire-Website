from __future__ import unicode_literals
from user_profile.models import AirpactUser
from django.db import models

# Create your models here.
class picture(models.Model):
	pic = models.ImageField(upload_to = 'pictures/')
	uploaded = models.DateTimeField(auto_now_add = True)
	description = models.TextField(default = "")
	user = models.ForeignKey(AirpactUser, on_delete=models.CASCADE)
	#visualRange = models.FloatField(null=False)

	def __str__(self):
		return self.description