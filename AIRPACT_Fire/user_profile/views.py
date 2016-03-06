from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from user_profile.models import UserProfile
from forms import UserProfileForm



@login_required
def user_profile(request):
	if(request.method == 'POST'):
		form = UserProfileForm(request.POST, instance=request.user.profile)


# Create your views here.
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
		return HttpResponseRedirect('/user_profile/loggedin')
	else:
		return HttpResponseRedirect('/user_profile/invalid')

def loggedin(request):
	return render_to_response()

def invalid_login(request):
	return render_to_response()


def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_success')
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()

	return render_to_response('register.html', args)
