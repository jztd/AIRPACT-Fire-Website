from __future__ import unicode_literals
from user_profile.models import AirpactUser
from django.db import models
from PIL import Image, ImageOps, ImageDraw
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage as storage
from TwoTargetContrast import TwoTargetContrast
import math
import os
# Create your models here.
class picture(models.Model):
	pic = models.ImageField(upload_to = 'pictures/')
	thumbnail = models.ImageField(upload_to = 'thumbnails/', null=True, blank=True)
	pictureWithCircles = models.ImageField(upload_to = 'circles/', null=True, blank=True)
	uploaded = models.DateTimeField(auto_now_add = True)
	description = models.TextField(default = "")
	user = models.ForeignKey(AirpactUser, on_delete=models.CASCADE)
	vr = models.FloatField(null=False, default=0)
	vrUnits = models.CharField(null = True, default = 'K', max_length = 1)
	twoTargetContrastVr = models.FloatField(null=True,default=0)
	highColor = models.IntegerField(null=False , default=0)
	highX = models.FloatField(null=False, default=0)
	highY= models.FloatField(null=False, default=0)
	farTargetDistance = models.FloatField(null = True, default = 0)
	nearTargetDistance = models.FloatField(null = True, default = 0)
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
		self.pic.seek(0)
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
		highCords = [(self.highX-int(math.ceil(math.sqrt(20000))), self.highY-int(math.ceil(math.sqrt(20000)))),(self.highX+int(math.ceil(math.sqrt(20000))), self.highY+int(math.ceil(math.sqrt(20000))))]
		lowCords = [(self.lowX-int(math.ceil(math.sqrt(20000))), self.lowY-int(math.ceil(math.sqrt(20000)))),(self.lowX+int(math.ceil(math.sqrt(20000))), self.lowY+int(math.ceil(math.sqrt(20000))))]

		#open original image
		self.pic.seek(0)
		OriginalImage = Image.open(StringIO(self.pic.read()))

		#open a new drawing object with our image
		editor = ImageDraw.Draw(OriginalImage)

		#draw the cricles
		for i in range(0,10):
			outline_value = (0,0,0)
			if i > 5:
				outline_value = (255,255,255)
			editor.ellipse([highCords[0][0]-i,highCords[0][1]-i,highCords[1][0]+i,highCords[1][1]+i], outline=outline_value)
			editor.ellipse([lowCords[0][0]-i,lowCords[0][1]-i,lowCords[1][0]+i,lowCords[1][1]+i], outline=outline_value)

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
		print("CIRCLES URL IS:")
		print(self.pictureWithCircles.url)
	
	def findTwoTargetContrastVr(self):
		self.pic.seek(0)
		#open image
		image = Image.open(StringIO(self.pic.read()))

		#convert to RGB values for each pixel
		pixelData = image.convert('RGB')

		#set up containers for red green and blue for each target
		hRed = []
		hGreen = []
		hBlue = []
		lRed = []
		lGreen = []
		lBlue = []

		#find the top left of the bounding box (this is based on the 200x200 px that we have all agreed upon it's probalbly going to have to change)
		newHX = int(self.highX - 100)
		newHY = int(self.highY - 100)
		newLX = int(self.lowX - 100)
		newLY = int(self.lowY - 100)

		#process high or "Far" target first
		for y in range(newHY, newHY+200):
			for x in range(newHX, newHX+200):
				R,G,B = pixelData.getpixel((x,y))
				hRed.append(R)
				hGreen.append(G)
				hBlue.append(B)

		#do the same for the low or "close" target
		for y in range(newLY, newLY+200):
			for x in range(newLX, newLX+200):
				R,G,B = pixelData.getpixel((x,y))
				lRed.append(R)
				lGreen.append(G)
				lBlue.append(B)

		#now we need to run the function 3 times one for each color band then average them together
		vrR = TwoTargetContrast(hRed,lRed,self.farTargetDistance,self.nearTargetDistance)
		vrG = TwoTargetContrast(hGreen,lGreen,self.farTargetDistance,self.nearTargetDistance)
		vrB = TwoTargetContrast(hBlue,lBlue,self.farTargetDistance,self.nearTargetDistance)

		#finally average the numbers togther
		self.twoTargetContrastVr = (abs((vrR[0] + vrG[0] + vrB[0]) / 3))
	
	def save(self):

		print("saving circles")
		self.generateCircles()
		print("saving thumbnail")
		self.generateThumbnail()
		print("finding vr")
		self.findTwoTargetContrastVr()
		print("trying to save")
		super(picture,self).save()

	
	def __str__(self):
		return self.description

# We called them tags, they are really the string representation of where a picture was taken uploaded by the user
# That sounds like an intro to a movie
# I need sleep
class tag(models.Model):
	picture = models.ForeignKey(picture, on_delete=models.CASCADE)
	text = models.TextField(null=False)