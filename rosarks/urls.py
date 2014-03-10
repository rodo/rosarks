from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^bicycle_rental/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/(?P<precision>\d+\.?\d{0,2}\d*)/$', 'rosarks.amenity.views.bicycle_rental_precision'),
    url(r'^bicycle_rental/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/$', 'rosarks.amenity.views.bicycle_rental'),
    url(r'^subway_station/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/(?P<precision>\d+\.?\d{0,2}\d*)/$', 'rosarks.amenity.views.subway_station_precision'),
    url(r'^subway_station/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/$', 'rosarks.amenity.views.subway_station'),

    url(r'^tramway_station/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/(?P<precision>\d+\.?\d{0,2}\d*)/$', 'rosarks.amenity.views.tram_station_precision'),
    url(r'^tramway_station/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/$', 'rosarks.amenity.views.tram_station'),

    url(r'^bus_stop/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/(?P<precision>\d+\.?\d{0,2}\d*)/$', 'rosarks.amenity.views.bus_stop_precision'),
    url(r'^bus_stop/(?P<lon>-?\d+\.?\d{0,5})\d*/(?P<lat>-?\d+\.?\d{0,5}\d*)/$', 'rosarks.amenity.views.bus_stop'),


    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^howto/$', TemplateView.as_view(template_name='howto.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html')),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
)
