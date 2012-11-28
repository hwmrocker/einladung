from django.conf.urls import patterns, include, url

urlpatterns = patterns('einladung.views',
    #url(r'gast/id(?P<person_secret>\d+)', 'einladung.views.zusage'),
    url(r'g/(?P<hash>[0-9a-zA-Z]+)', 'goto'),
    url(r'^gast/(?P<person_secret>[0-9a-zA-Z]+)/', include('einladung.gast_urls')),
    # haus suche
    # info seiten / kirche / essen / feier
    # upload csv
    # download csv
)