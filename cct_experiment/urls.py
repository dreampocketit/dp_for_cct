from django.conf.urls import patterns, url
from cct_experiment import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^get_sys_state', views.get_sys_state, name='get_sys_state'),
    url(r'^start_record', views.start_record, name='start_record'),
    url(r'^write_data', views.write_data, name='write_data'),
)      
