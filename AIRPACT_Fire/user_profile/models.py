from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	bio = models.TextField(max_length=1000, null=True, blank=True)
from django.db.models.signals import post_save
from django.dispatch import receiver

#User.profile = property( lamda u: UserProfile.objects.get_or_create(user=u)[0])

