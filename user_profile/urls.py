
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_page$', views.admin_page, name="adminPage"),
    url(r'^$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^auth$', views.auth_view),
    url(r'^register$', views.register_user, name='register'),
    url(r'^loggedin$', views.loggedin),
    url(r'^invalid$', views.invalid_login),
    url(r'^appauth$',views.user_app_auth),
    url(r'^register_success$', views.register_success),
    url(r'^profile/edit/$', views.edit_profile, name="edit_profile"),
    url(r'^profile/manage_pictures/$', views.manage_pictures, name="manage_pictures"),
    url(r'^profile/(?P<name>[-A-Za-z]+)/$', views.view_profile, name="view_profile"),
    url(r'^profile/(?P<name>[-A-Za-z]+)/(?P<page>\d+)/$', views.view_profile, name="view_profile"),
    
    #include('file_upload.urls')
    #more to come...
]