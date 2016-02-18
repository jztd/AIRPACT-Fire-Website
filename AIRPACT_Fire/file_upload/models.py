from __future__ import unicode_literals

from django.db import models

# Create your models here.
class picture(models.Model):
	pic = models.ImageField(upload_to = 'pictures/')
	uploaded = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.uploaded