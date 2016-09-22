from __future__ import unicode_literals
from user_profile.models import AirpactUser
from django.db import models
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os
# Create your models here.
class picture(models.Model):
	pic = models.ImageField(upload_to = 'static/pictures/')
	thumbnail = models.ImageField(upload_to = 'static/thumbnails/', null=True, blank=True)
	uploaded = models.DateTimeField(auto_now_add = True)
	description = models.TextField(default = "")
	user = models.ForeignKey(AirpactUser, on_delete=models.CASCADE)
	vr = models.FloatField(null=False, default=0)
	highColor = models.IntegerField(null=False , default=0)
	highX = models.FloatField(null=False, default=0)
	highY= models.FloatField(null=False, default=0)
	lowColor = models.IntegerField(null=False, default=0)
	geoX = models.FloatField(default = 0)
	geoY = models.FloatField(default = 0)

	def generateThumbnail(self):
		thumbnailSize = (200,200)
		imageType = self.pic.file.content_type

		#see what kind of file we are dealing with 
		print(imageType)
		if imageType == "image/jpeg":
			pilImageType = "jpeg"
			fileExtension = "jpg"
		elif imageType == "image/png":
			pilImageType = "png"
			fileExtension = "png"

		#open big picture into PIL
		OriginalImage = Image.open(StringIO(self.pic.read()))
		OriginalImage.thumbnail(thumbnailSize, Image.ANTIALIAS)
		tempHandle = StringIO()
		OriginalImage.save(tempHandle, pilImageType)
		tempHandle.seek(0)
		suf = SimpleUploadedFile(os.path.split(self.pic.name)[-1],tempHandle.read(),content_type=imageType)
		self.thumbnail.save('%s.%s'%(os.path.splitext(suf.name)[0],fileExtension), suf, save=False)






	def save(self):

		self.generateThumbnail()
		super(picture,self).save()
	def __str__(self):
		return self.description

# THE BITCHIN TIGGLE TAG
class tag(models.Model):
	picture = models.ForeignKey(picture, on_delete=models.CASCADE)
	text = models.TextField(null=False)