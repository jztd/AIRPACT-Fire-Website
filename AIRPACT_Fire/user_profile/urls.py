
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^auth$', views.auth_view),
    url(r'^register$', views.register_user),
    url(r'^loggedin$', views.loggedin),
    url(r'^invalid$', views.invalid_login),
    url(r'^appauth$',views.user_app_auth),
    url(r'^register_success$', views.register_success),
    #include('file_upload.urls')
    #more to come...
]