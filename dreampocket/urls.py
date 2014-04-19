from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 


    url(r'^cct_experiment/', include('cct_experiment.urls')), 
    # Allow the URLs beginning with /captcha/ to be handled by
    # the urls.py of captcha module from 'django-simple-captcha'
    #url(r'^captcha/', include('captcha.urls')),
)
