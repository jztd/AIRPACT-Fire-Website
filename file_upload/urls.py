from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^test$',views.test, name='test'),
    url(r'^delete/(?P<id>\d+)/$',views.delete_picture, name="delete_picture")
]