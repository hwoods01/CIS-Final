from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^trails/(?P<pk>\w+)/$', views.trail_detail, name='trail_detail'),
    url(r'^$', views.search, name='search'),
    url(r'^all$', views.all, name='all'),
]