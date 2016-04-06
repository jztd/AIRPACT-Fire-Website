from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

from file_upload.models import picture
from convos.models import convoPage

def index(request):
	return render_to_response('index2.html', context_instance=RequestContext(request))



def test(request):
	return render_to_response('hello.html', RequestContext(request))

def gallery(request):
	pictures = picture.objects.all()

	conversations = convoPage.objects.all()
	return render_to_response('gallery.html', {'pics': pictures, 'conversations':conversations}, context_instance=RequestContext(request))

