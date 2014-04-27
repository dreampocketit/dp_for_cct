from django.conf.urls import patterns, url
from for_android import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^get_data', views.get_data, name='get_data'),
)      
