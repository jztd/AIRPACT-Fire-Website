from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from file_upload.models import picture
from convos.models import convoPage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from user_profile.models import AirpactUser

def index(request):
	newestPictures = picture.objects.all().order_by("-uploaded")[:4]
	return render_to_response('index2.html', {'newestPictures' : newestPictures}, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def admin_page(request):
	if request.user.is_custom_admin is False:
		return HttpResponseRedirect('/')
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')

	users = AirpactUser.objects.all()
	if(request.method == 'POST'):
		print(request.POST)
		username = request.POST.get("ourUser",False)
		user = AirpactUser.objects.get(username=username)
		the_type = request.POST['the_type']
		
		if(the_type == "certify"):
			user.is_certified = True 
			user.save()

		if(the_type == "uncertify"):
			user.is_certified = False 
			user.save()

		if(the_type == "make_admin"):
			user.is_custom_admin = True
			user.save() 

		if(the_type == "unmake_admin"):
			user.is_custom_admin = False
			user.save() 

		if(the_type == "delete"):
			user.delete()

	return render_to_response('custom_admin_page.html', {'users': users})

def uncertified(request):
	return render_to_response('not_certified.html')

def test(request):
	return render_to_response('hello.html', RequestContext(request))

def gallery(request, page = 1, sort="dateu"):
	allpictures = picture.objects.all()
	if sort == "dateu":
		allpictures = allpictures.order_by('-uploaded')
	elif sort == "dated":
		allpictures = allpictures.order_by('uploaded')
	elif sort == "vru":
		allpictures = allpictures.order_by('-vr')
	elif sort == "vrd":
		allpictures = allpictures.order_by('vr')
	paginator = Paginator(allpictures, 12) #show 12 per page
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		pictures = paginator.page(1)
	except EmptyPage:
		pictures = paginator.page(paginator.num_pages)

	return render_to_response('gallery.html', {'pictures': pictures, 'sort' : sort }, context_instance=RequestContext(request))

def downloads(request):
	return render_to_response("downloads.html", context_instance=RequestContext(request))

