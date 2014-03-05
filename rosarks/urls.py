from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^bicycle_rental/(?P<lon>-?\d+\.\d+)/(?P<lat>-?\d+\.\d+)$', 'rosarks.amenity.views.bicycle_rental'),
    # Examples:
    # url(r'^$', 'rosarks.views.home', name='home'),    
    #url(r'^admin/', include(admin.site.urls)),
)
