from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^bicycle_rental/(?P<lon>-?\d+\.\d+)/(?P<lat>-?\d+\.\d+)$', 'rosarks.amenity.views.bicycle_rental'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html')),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
)
