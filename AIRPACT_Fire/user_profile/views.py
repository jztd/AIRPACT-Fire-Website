from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user_profile.models import UserProfile

from forms import MyRegistrationForm



@login_required
def user_profile(request):
	if(request.method == 'POST'):
		form = UserProfileForm(request.POST, instance=request.user.profile)



def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password' , '')

	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/user/loggedin')
	else:
		return HttpResponseRedirect('/user/invalid')

def loggedin(request):
	return render_to_response('loggedin.html')

def invalid_login(request):
	return render_to_response('invalid.html')

@csrf_exempt
def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/user/register_success')
		else:
			return HttpResponseRedirect('/user/register',{'form':form}) 

	form = MyRegistrationForm()
	return render_to_response('register.html', {'form':form, 'form_errors':form.errors} )

@csrf_exempt
def register_success(request): 
	return render_to_response('register_success.html')