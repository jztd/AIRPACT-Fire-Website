from __future__ import unicode_literals
from user_profile.models import AirpactUser
from django.db import models
from PIL import Image, ImageOps, ImageDraw
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from mimetypes import MimeTypes
import os
# Create your models here.
class picture(models.Model):
	pic = models.ImageField(upload_to = 'static/pictures/')
	thumbnail = models.ImageField(upload_to = 'static/thumbnails/', null=True, blank=True)
	pictureWithCircles = models.ImageField(upload_to = 'static/circles/', null=True, blank=True)
	uploaded = models.DateTimeField(auto_now_add = True)
	description = models.TextField(default = "")
	user = models.ForeignKey(AirpactUser, on_delete=models.CASCADE)
	vr = models.FloatField(null=False, default=0)
	highColor = models.IntegerField(null=False , default=0)
	highX = models.FloatField(null=False, default=0)
	highY= models.FloatField(null=False, default=0)
	lowColor = models.IntegerField(null=False, default=0)
	lowX = models.FloatField(null=False, default=0)
	lowY = models.FloatField(null=False,default=0)
	geoX = models.FloatField(default = 46.7298)
	geoY = models.FloatField(default =  -117.181738)

	def generateThumbnail(self):
		thumbnailSize = (200,200)


		#see what kind of file we are dealing with 
		if self.pic.name.endswith(".jpg"):
			pilImageType = "jpeg"
			fileExtension = "jpg"
			djangoType = 'image/jpeg'
		elif self.pic.name.endswith(".png"):
			pilImageType = "png"
			fileExtension = "png"
			djangoType = 'image/png'

		#open big picture into PIL
		OriginalImage = Image.open(StringIO(self.pic.read()))
		OriginalImage.thumbnail(thumbnailSize, Image.ANTIALIAS)
		tempHandle = StringIO()
		background = Image.new('RGBA', thumbnailSize, (255,255,255,0))
		background.paste(OriginalImage,((thumbnailSize[0] - OriginalImage.size[0]) / 2, (thumbnailSize[1] - OriginalImage.size[1]) / 2))
		
		background.save(tempHandle, pilImageType)


		tempHandle.seek(0)
		suf = SimpleUploadedFile(os.path.split(self.pic.name)[-1],tempHandle.read(),content_type = djangoType)
		self.thumbnail.save('%s.%s'%(os.path.splitext(suf.name)[0],fileExtension), suf, save=False)


	# creates a copy of the image with the circle points drawn on them 
	def generateCircles(self):


		#see what kind of file we are dealing with 
		if self.pic.name.endswith(".jpg"):
			pilImageType = "jpeg"
			fileExtension = "jpg"
			djangoType = 'image/jpeg'
		elif self.pic.name.endswith(".png"):
			pilImageType = "png"
			fileExtension = "png"
			djangoType = 'image/png'

		#get the bounding boxes for each of the circles
		highCords = [(self.highY-100, self.highX-100),(self.highY+100, self.highX+100)]
		lowCords = [(self.lowY-100, self.lowX-100),(self.lowY+100, self.lowX+100)]

		#open original image
		OriginalImage = Image.open(StringIO(self.pic.read()))

		#open a new drawing object with our image
		editor = ImageDraw.Draw(OriginalImage)

		#draw the cricles
		editor.eclipse(highCords, outline=0)
		editor.eclipse(lowCords, outline=0)

		#get rid of the drawer
		del editor

		#create a place to hold the new image for a second
		tempHandle = StringIO()

		#write the image to the handler
		OriginalImage.save(tempHandle, pilImageType)
		tempHandle.seek(0)

		#save the image
		suf = SimpleUploadedFile(os.path.split(self.pic.name)[-1],tempHandle.read(),content_type=djangoType)
		self.pictureWithCircles.save('%s.%s'%(os.path.splitext(suf.name)[0],fileExtension), suf, save=False)


	def save(self):

		self.generateThumbnail(self)
		self.generateCircles(self)
		super(picture,self).save()
	
	def __str__(self):
		return self.description

# We called them tags, they are really the string representation of where a picture was taken uploaded by the user
class tag(models.Model):
	picture = models.ForeignKey(picture, on_delete=models.CASCADE)
	text = models.TextField(null=False)