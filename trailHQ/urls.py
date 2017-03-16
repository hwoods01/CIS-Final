from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^trails/(?P<pk>\w+)/$', views.trail_detail, name='trail_detail'),
    url(r'^$', views.all, name='all'),
]