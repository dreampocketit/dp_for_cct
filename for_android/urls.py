from django.conf.urls import patterns, url
from for_android import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^get_diff_data', views.get_diff_data, name='get_diff_data'),
    url(r'^get_easy_data', views.get_easy_data, name='get_easy_data'),
)      
