# Create your views here.
import json
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from rosarks.amenity.models import BicycleRental

#@cache_page(3600)
def bicycle_rental(request, lon, lat):
    """Return the main stats

    All bicycle rental at less than 1.42 kilometers
    """
    datas = []
    brs = BicycleRental.objects.all()

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    brs = BicycleRental.objects.filter(position__distance_lte=(pnt, D(km=1.42)))

    for br in brs:
        datas.append({'lon': br.position[0],
                      'lat': br.position[1],
                      'name': br.name,
                      'osmid': br.osmid,
                      'operator': br.operator,
                      'amenity': 'bicycle_rental'})

    return HttpResponse(json.dumps(datas),
                        mimetype='application/json')

