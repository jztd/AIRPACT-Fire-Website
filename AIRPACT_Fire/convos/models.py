from __future__ import unicode_literals
from django.db import models
from file_upload.models import picture
from user_profile.models import AirpactUser


# The model responsible for storing information about the convo page
class convoPage(models.Model):	 
	picture = models.ForeignKey(picture, on_delete=models.CASCADE)	
	description = models.TextField(default = "", blank = True)
	
	def __str__(self):
		return self.description



# a custom comments class! whoo! It has convo page
class comment(models.Model):
	convoPage = models.ForeignKey(convoPage, on_delete=models.CASCADE)
	text =  models.TextField(default = "", blank = True)

	def __str__(self):
		return self.description	