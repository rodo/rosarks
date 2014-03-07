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
from rosarks.amenity.models import TramStation, TramRoute, TramStop


def build_resulsts(status, request, lon, lat, precision, datas):
    """
    Return String
    """
    results = {'status' : status,
               'query': request.get_full_path(),
               'center': [lon,lat],
               'precision': precision,
               'nb_results': len(datas),
               'datas' : datas}

    return json.dumps(results)


def serve(request, results):
    """
    Return final result

    Look if requets is made in JSON or JSONP
    """
    try:
        callback = request.GET['callback']
        content = "{}({});".format(callback, results)
    except KeyError:
        content = results
        

    return HttpResponse(content, mimetype='application/json')    


@cache_page(30)
def bicycle_rental(request, lon, lat):
    return bicycle_rental_precision(request, lon, lat, settings.ROSARKS_DISTANCE_DEFAULT)

@cache_page(30)
def bicycle_rental_precision(request, lon, lat, precision):
    """Return the main stats

    All bicycle rental at less than 1.42 kilometers
    """
    precision = max(float(settings.ROSARKS_DISTANCE_MIN), float(precision))
    precision = min(float(settings.ROSARKS_DISTANCE_MAX), float(precision))

    datas = []

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    brs = BicycleRental.objects.filter(position__distance_lte=(pnt, D(m=precision))).distance(pnt).order_by('distance')[:10]

    for br in brs:
        datas.append({'lon': br.position[0],
                      'lat': br.position[1],
                      'distance': br.distance.m,
                      'name': br.name,
                      'osmid': br.osmid,
                      'operator': br.operator,
                      'amenity': 'bicycle_rental'})

    results = build_resulsts(0, request, lon, lat, precision, datas)

    return serve(request, results)


@cache_page(30)
def subway_station(request, lon, lat):
    """Subway stations

    Each subway station with line information
    """
    return subway_station_precision(request, lon, lat, settings.ROSARKS_DISTANCE_DEFAULT)


@cache_page(30)
def subway_station_precision(request, lon, lat, precision):

    precision = max(float(settings.ROSARKS_DISTANCE_MIN), float(precision))
    precision = min(float(settings.ROSARKS_DISTANCE_MAX), float(precision))

    datas = []

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    stations = SubwayStation.objects.filter(position__distance_lte=(pnt, D(m=precision))).distance(pnt).order_by('distance')[:10]

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
                      'distance': station.distance.m,
                      'name': station.name,
                      'osmid': station.osmid,
                      'amenity': 'subway_station',
                      'subway_lines': lines})

    results = build_resulsts(0, request, lon, lat, precision, datas)

    return serve(request, results)


@cache_page(30)
def tram_station(request, lon, lat):
    """Tram stations

    Each tram station with line information
    """
    return tram_station_precision(request, lon, lat, settings.ROSARKS_DISTANCE_DEFAULT)


@cache_page(30)
def tram_station_precision(request, lon, lat, precision):

    precision = max(float(settings.ROSARKS_DISTANCE_MIN), float(precision))
    precision = min(float(settings.ROSARKS_DISTANCE_MAX), float(precision))

    datas = []

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    stations = TramStation.objects.filter(position__distance_lte=(pnt, D(m=precision))).distance(pnt).order_by('distance')[:10]

    for station in stations:
        lines = []
        stops = TramStop.objects.filter(station=station)

        for stop in stops:
            route = TramRoute.objects.get(pk=stop.route.id)
            lines.append({"name": route.name,
                          "ref": route.ref,
                          "colour": route.colour})

        datas.append({'lon': station.position[0],
                      'lat': station.position[1],
                      'distance': station.distance.m,
                      'name': station.name,
                      'osmid': station.osmid,
                      'amenity': 'tram_station',
                      'tram_lines': lines})

    results = build_resulsts(0, request, lon, lat, precision, datas)

    return serve(request, results)

