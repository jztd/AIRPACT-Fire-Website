from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from file_upload.models import picture
from convos.models import convoPage

def index(request):
	return render_to_response('index2.html', context_instance=RequestContext(request))



def test(request):
	return render_to_response('hello.html', RequestContext(request))

def gallery(request, page = 1):
	allpictures = picture.objects.all()
	paginator = Paginator(allpictures, 12) #show 12 per page
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		pictures = paginator.page(1)
	except EmptyPage:
		pictures = paginator.page(paginator.num_pages)

	return render_to_response('gallery.html', {'pictures': pictures}, context_instance=RequestContext(request))

