import json
import urllib
from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from file_upload.models import picture
from convos.models import convoPage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from user_profile.models import AirpactUser
from file_upload.forms import GallerySortForm

def index(request):
	newestPictures = picture.objects.all().order_by("-uploaded")[:20]
	return render_to_response('index2.html',{'newestPictures' : newestPictures}, context_instance=RequestContext(request))
def main(request):
	return render_to_response('welcome.html', context_instance=RequestContext(request))
def forum(request):
	return render_to_response('forum.html', context_instance=RequestContext(request))

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

def gallery(request, page = 1):
	allpictures = picture.objects.all().order_by("-uploaded")
	form = GallerySortForm();
	if request.method == 'POST':
		sortByList=[];
		form = GallerySortForm(request.POST)
		if form.is_valid():
			if form.cleaned_data.get("uploaded") == "asc":
				allpictures = allpictures.order_by("uploaded")
			elif form.cleaned_data.get("uploaded") == "desc":
				allpictures = allpictures.order_by("-uploaded")
			elif form.cleaned_data.get("vr") == "asc":
				allpictures = allpictures.order_by("vr")
			elif form.cleaned_data.get("vr") == "desc":
				allpictures = allpictures.order_by("-vr")
			# if form.cleaned_data.get("location") != "":.
			# 	allpictures.filter(text = form.cleaned_data.get("location"))
			if form.cleaned_data.get("date") != "":
				d = datetime.strptime(form.cleaned_data.get("date"),"%m/%d/%Y")
				print(form.cleaned_data.get("date"))
				print(allpictures[0].uploaded)
				allpictures = allpictures.filter(uploaded__month=d.month,uploaded__day=d.day,uploaded__year=d.year)


	# if sort == "dateu":
	# 	allpictures = allpictures.order_by('-uploaded')
	# elif sort == "dated":
	# 	allpictures = allpictures.order_by('uploaded')
	# elif sort == "vru":
	# 	allpictures = allpictures.order_by('-vr')
	# elif sort == "vrd":
	# 	allpictures = allpictures.order_by('vr')

	paginator = Paginator(allpictures, 12) #show 12 per page
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		pictures = paginator.page(1)
	except EmptyPage:
		pictures = paginator.page(paginator.num_pages)

	return render_to_response('gallery.html', {'pictures': pictures, 'form': form}, context_instance=RequestContext(request))

def downloads(request):
	return render_to_response("downloads.html", context_instance=RequestContext(request))

def about(request):
	newestPictures = picture.objects.all().order_by("-uploaded")[:4]
	return render_to_response("about.html", {'newestPictures' : newestPictures}, context_instance=RequestContext(request))
@csrf_exempt
def getPythonScripts(request):
	opener = urllib.URLopener()
	scriptURL = "https://s3-us-west-2.amazonaws.com/airpactfire/static/media/scripts/alg1.py"
	responseData = {}
	scriptFile = opener.open(scriptURL)

	responseData['alg1'] = scriptFile.read()
	return HttpResponse(json.dumps(responseData), content_type="application/json")




