from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user_profile.models import AirpactUser
from user_profile.models import AuthToken
from file_upload.models import picture
from django.template import RequestContext
from forms import UserCreationForm
from forms import EditProfileForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from convos.models import convoPage
import json
import random
import string

@login_required
def user_profile(request):
	if(request.method == 'POST'):
		form = UserProfileForm(request.POST, instance=request.user.profile)

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

@login_required
def logout(request):
	auth.logout(request)
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)

	# # For now, do not ask for the email
	# #email = request.POST['email']

	# print("\n ! !  This is the post information from login:")
	# print(request.POST)
	# print("\n ! !  This is the password:")
	# print(password)


		if user is not None:
		   auth.login(request, user)
		   return HttpResponseRedirect('/user/loggedin')
		else:
			return HttpResponseRedirect('/user/invalid')
	return HttpResponse("DONT GO HERE")
	
def loggedin(request):
	return render_to_response('loggedin.html')

def invalid_login(request):
	return render_to_response('invalid.html')


# Register/ Create a new user
def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/user/register_success')
		else:
			return render_to_response('register.html',  {'form':form}, context_instance=RequestContext(request) )

	form = UserCreationForm()
	return render_to_response('register.html',  {'form':form}, context_instance=RequestContext(request) )


def register_success(request): 
	return render_to_response('register_success.html', {'message': "successfull registration! "}, context_instance=RequestContext(request))

@csrf_exempt
def user_app_auth(request):
	if request.method == 'POST':
		userdata = json.loads(request.body)
		user = auth.authenticate(username=userdata['username'], password=userdata['password'] )
		response_data = {}
		if user is not None:
			#generate secret key
			secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(22))
			secretKey = AuthToken(token = secret)
			secretKey.save()
			response_data['isUser'] = 'true'
			response_data['secretKey'] = secret
		else:
			response_data['isUser'] = 'false'
			response_data['secretKey'] = ''
		print(json.dumps(response_data))
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		return HttpResponse("HI")


def view_profile(request, name, page = 1):
	# we need to get the current user info
	# send it to the view...so lets do that I guess
	thisuser = False
	if request.user.username == name:
		thisuser = True
	user = AirpactUser.objects.get(username = name)
	userpictures = picture.objects.filter(user = user)
	paginator = Paginator(userpictures, 12) #show 12 per page
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		pictures = paginator.page(1)
	except EmptyPage:
		pictures = paginator.page(paginator.num_pages)
	return render_to_response('user_profile.html', {'pictures' : pictures, 'profile_user':user, 'thisuser':thisuser}, context_instance=RequestContext(request))

@login_required
def edit_profile(request):
	userob = AirpactUser.objects.get(username=request.user.username)
	if request.method == 'POST':
		# do stuff to save the new user data
		form = EditProfileForm(request.POST)
		if form.is_valid():
			userob.first_name = form.cleaned_data.get('first_name')
			userob.last_name = form.cleaned_data.get('last_name')
			userob.email = form.cleaned_data.get('email')
			userob.bio = form.cleaned_data.get('bio')
			userob.save()
		#reidrect back to their profile
		return HttpResponseRedirect('/user/profile/'+request.user.username+'/')
	form = EditProfileForm(instance=userob)
	pictures = picture.objects.filter(user = userob)
	return render_to_response('edit_profile.html', {'user': request.user, 'form':form, 'pictures': pictures}, context_instance=RequestContext(request))

@login_required
def manage_pictures(request):
	userob = AirpactUser.objects.get(username=request.user.username)
	pictures = picture.objects.filter(user= userob)
	return render_to_response('manage_pictures.html', {'pictures': pictures}, context_instance=RequestContext(request))
	