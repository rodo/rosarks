# This file is part of Rosarks.

# Rosarks is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.


# Rosarks is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with Rosarks. If not, see <http://www.gnu.org/licenses/>.
"""
Views definition for resume
"""
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from rosarks.amenity.models import BicycleRental
from rosarks.amenity.models import SubwayStation, SubwayRoute, SubwayStop


@cache_page(30)
def bicycle_rental(request, lon, lat):
    """Return the main stats

    All bicycle rental at less than 1.42 kilometers
    """
    distance = settings.ROSARKS_DISTANCE_DEFAULT
    datas = []
    brs = BicycleRental.objects.all()

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    brs = BicycleRental.objects.filter(position__distance_lte=(pnt, D(m=distance)))

    for br in brs:
        datas.append({'lon': br.position[0],
                      'lat': br.position[1],
                      'name': br.name,
                      'osmid': br.osmid,
                      'operator': br.operator,
                      'amenity': 'bicycle_rental'})

    results = {'status' : 0,
               'query': request.get_full_path(),
               'nb_results': len(datas),
               'datas' : datas}

    return HttpResponse(json.dumps(results),
                        mimetype='application/json')


@cache_page(30)
def subway_station(request, lon, lat):
    """Subway stations

    Each subway station with line information
    """
    distance = settings.ROSARKS_DISTANCE_DEFAULT
    datas = []

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    stations = SubwayStation.objects.filter(position__distance_lte=(pnt, D(m=distance)))

    for station in stations:
        lines = []
        stops = SubwayStop.objects.filter(station=station)

        for stop in stops:
            route = SubwayRoute.objects.get(pk=stop.route.id)
            lines.append({"name": route.name,
                          "ref": route.ref,
                          "colour": route.colour})

        datas.append({'lon': station.position[0],
                      'lat': station.position[1],
                      'name': station.name,
                      'osmid': station.osmid,
                      'amenity': 'subway_station',
                      'lines': lines})

    results = {'status' : 0,
               'query': request.get_full_path(),
               'nb_results': len(datas),
               'datas' : datas}

    return HttpResponse(json.dumps(results),
                        mimetype='application/json')

