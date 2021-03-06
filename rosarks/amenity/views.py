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
from rosarks.amenity.models import BusStop, BusRoute, BusRouteStop


def build_results(status, request, lon, lat, precision, datas):
    """
    Return String
    """
    try:
        limit = min(10, int(request.GET['limit']))
    except:
        limit = 10

    results = {'status': status,
               'query': request.get_full_path(),
               'center': [lon, lat],
               'precision': precision,
               'nb_results': len(datas),
               'datas': datas[:limit]}

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


def safe_precision(precision):
    precision = max(float(settings.ROSARKS_DISTANCE_MIN), float(precision))
    precision = min(float(settings.ROSARKS_DISTANCE_MAX), float(precision))

    return precision


@cache_page(3600)
def bicycle_rental(request, lon, lat):
    try:
        precision = request.GET['precision']
    except:
        precision = settings.ROSARKS_DISTANCE_DEFAULT

    return bicycle_rental_precision(request, lon, lat, precision)


@cache_page(3600)
def bicycle_rental_precision(request, lon, lat, precision):
    """Return the main stats

    All bicycle rental at less than 1.42 kilometers
    """
    precision = safe_precision(precision)
    datas = []

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    brs = BicycleRental.objects.filter(position__distance_lte=(pnt, D(m=precision))).distance(pnt).order_by('distance')[:10]

    for br in brs:
        datas.append({'lon': br.position[0],
                      'lat': br.position[1],
                      'distance': round(br.distance.m, 2),
                      'name': br.name,
                      'osmid': br.osmid,
                      'operator': br.operator,
                      'amenity': 'bicycle_rental'})

    results = build_results(0, request, lon, lat, safe_precision(precision), datas)

    return serve(request, results)


@cache_page(3600)
def subway_station(request, lon, lat):
    """Subway stations

    Each subway station with line information
    """
    try:
        precision = request.GET['precision']
    except:
        precision = settings.ROSARKS_DISTANCE_DEFAULT

    return subway_station_precision(request, lon, lat, precision)


@cache_page(3600)
def subway_station_precision(request, lon, lat, precision):
    """
    Subways
    """
    precision = safe_precision(precision)
    datas = []

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    stations = SubwayStation.objects.filter(position__distance_lte=(pnt, D(m=precision))).distance(pnt).order_by('distance')[:10]

    for station in stations:
        lines = []
        last = ""
        stops = SubwayStop.objects.filter(station=station)

        for stop in stops:
            route = SubwayRoute.objects.get(pk=stop.route.id)
            # try to remove duplicated datas
            key = u"{}{}{}".format(route.name, route.ref, route.colour)
            if key != last:
                lines.append({"name": route.name,
                              "ref": route.ref,
                              "colour": route.colour})
                last = key

        datas.append({'lon': station.position[0],
                      'lat': station.position[1],
                      'distance': round(station.distance.m, 2),
                      'name': station.name,
                      'osmid': station.osmid,
                      'amenity': 'subway_station',
                      'subway_lines': lines})

    results = build_results(0, request, lon, lat, precision, datas)

    return serve(request, results)


@cache_page(3600)
def tram_station(request, lon, lat):
    """Tram stations

    Each tram station with line information
    """
    try:
        precision = request.GET['precision']
    except:
        precision = settings.ROSARKS_DISTANCE_DEFAULT

    return tram_station_precision(request, lon, lat, precision)


@cache_page(3600)
def tram_station_precision(request, lon, lat, precision):
    """Tramway station
    """
    precision = safe_precision(precision)
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
                      'distance': round(station.distance.m, 2),
                      'name': station.name,
                      'osmid': station.osmid,
                      'amenity': 'tram_station',
                      'tram_lines': lines})

    results = build_results(0, request, lon, lat, precision, datas)

    return serve(request, results)


@cache_page(3600)
def bus_stop(request, lon, lat):
    """Tram stations

    Each tram station with line information
    """
    try:
        precision = request.GET['precision']
    except:
        precision = settings.ROSARKS_DISTANCE_DEFAULT

    return bus_stop_precision(request, lon, lat, precision)


@cache_page(3600)
def bus_stop_precision(request, lon, lat, precision):
    """
    Bus stop
    """
    precision = safe_precision(precision)
    datas = []

    pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))

    stations = BusStop.objects.filter(position__distance_lte=(pnt, D(m=precision))).distance(pnt).order_by('distance')[:10]

    for station in stations:
        lines = []
        last = None
        stops = BusRouteStop.objects.filter(stop=station)

        for stop in stops:
            route = BusRoute.objects.get(pk=stop.route.id)
            key = u"{}{}{}".format(route.name, route.ref, route.colour)
            if key != last:
                lines.append({"name": route.name,
                              "ref": route.ref,
                              "operator": route.operator,
                              "colour": route.colour})
                last = key

        datas.append({'lon': station.position[0],
                      'lat': station.position[1],
                      'distance': round(station.distance.m, 2),
                      'name': station.name,
                      'osmid': station.osmid,
                      'amenity': 'bus_stop',
                      'bus_lines': lines})

    results = build_results(0, request, lon, lat, precision, datas)

    return serve(request, results)
