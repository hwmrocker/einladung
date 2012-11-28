from django.conf.urls import patterns, include, url

urlpatterns = patterns('einladung.views',
    url(r'^$', 'zusage'),
    url(r'^privacy/$', 'privacy'),
    #url(r'^edit')
)