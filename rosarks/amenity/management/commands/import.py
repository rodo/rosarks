#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Import bicycle_rental

  <node id="60751375" lat="48.8652569" lon="2.3516674">
    <tag k="amenity" v="bicycle_rental"/>
    <tag k="capacity" v="34"/>
    <tag k="name" v="Sebastopol Grenata - 12 Rue Grenata - 75002 Paris"/>
    <tag k="network" v="Vélib’"/>
    <tag k="operator" v="JCDecaux"/>
    <tag k="ref" v="2001"/>
  </node>
"""
import sys
import json
from imposm.parser import OSMParser
from django.core.management.base import BaseCommand
from django.db import IntegrityError 
from rosarks.amenity.models import BicycleRental, BusStop, BusRoute, BusRouteStop
from rosarks.amenity.models import SubwayStation, SubwayRoute, SubwayStop
from rosarks.amenity.models import TramStation, TramRoute, TramStop


class Command(BaseCommand):
    help = 'Import data in file [ARG]'

    def handle(self, *args, **options):
        """
        Handle the munin command
        """
        fpath = sys.argv[2]
        self.stdout.write('import {}\n'.format(fpath))

        # instantiate counter and parser and start parsing
        chker = RosaParse()
        p = OSMParser(concurrency=4, 
                      nodes_callback=chker.pnodes,
                      relations_callback=chker.prelations)

        # Read filename on cmd arg
        p.parse(fpath)

class RosaParse(object):
    """The OSM parser rules
    """
    def pnodes(self, nodes):
        """Parse the nodes
        """
        for osmid, tags, coord in nodes:
            if 'amenity' in tags:
                if tags['amenity'] == "bicycle_rental":
                    create_bicycle_rental(osmid, tags, coord)

            if 'highway' in tags:
                if tags['highway'] == "bus_stop":
                    create_bus_stop(osmid, tags, coord)

            if 'railway' in tags:
                if 'station' in tags:
                    if tags['railway'] == "station" and tags['station'] == 'subway':
                        create_subway_station(osmid, tags, coord)
                if tags['railway'] == "tram_stop":
                        create_tram_station(osmid, tags, coord)

    def prelations(self, relations):
        """Parse the relations
        """
        for osmid, tags, members in relations:
            if 'type' in tags and 'route' in tags:
                if tags['type'] == 'route':
                    self.routes(osmid, tags, members)

    def routes(self, osmid, tags, members):
        """
        Route for bus/subway and tramway
        """
        if tags['route'] == 'subway':
            create_subway_route(osmid, tags, members)
            for member in members:
                if member[1] == 'node' and member[2] == 'stop':
                    create_subway_stop(osmid, member[0])
        if tags['route'] == 'tram' or tags['route'] == 'trolleybus':
            create_tram_route(osmid, tags, members)
            for member in members:
                if member[1] == 'node' and member[2] == 'stop':
                    create_tram_stop(osmid, member[0])
        if tags['route'] == 'bus':
            create_bus_route(osmid, tags, members)
            for member in members:
                if member[1] == 'node' and member[2] == 'stop':
                    create_busroute_stop(osmid, member[0])


def create_bicycle_rental(osmid, tags, coord):
    position = 'POINT({} {})'.format(coord[0], coord[1])
    b = BicycleRental(osmid=osmid, position=position)

    try:
        b.capacity = int(tags['capacity'])
    except:
        pass

    try:
        operator = tags['operator']
        b.operator = operator[:50]
    except KeyError:
        pass

    try:
        b.name = tags['name']
    except KeyError:
        pass
    b.save()

def create_subway_station(osmid, tags, coord):
    position = 'POINT({} {})'.format(coord[0], coord[1])
    b = SubwayStation(osmid=osmid, position=position)

    try:
        b.name = tags['name']
    except KeyError:
        pass

    b.save()

def create_subway_route(osmid, tags, members):
    """A subway route is in double in database, one per direction
    """
    b = SubwayRoute(osmid=osmid)

    try:
        b.name = tags['name']
    except KeyError:
        pass

    try:
        operator = tags['operator']
        b.operator = operator[:50]
    except KeyError:
        pass

    try:
        b.colour = tags['colour']
        if len(b.colour) > 10:
            b.colour = b.colour[:10]
    except KeyError:
        pass

    try:
        b.ref = tags['ref']
        if len(b.ref) > 10:
            b.ref = b.ref[:10]
    except KeyError:
        pass
    b.save()

def create_subway_stop(route_id, station_id):
    """A subway route is in double in database, one per direction
    """
    station = SubwayStation.objects.filter(osmid=station_id)
    route = SubwayRoute.objects.filter(osmid=route_id)

    if (len(station) == 1 and len(route) == 1):
        try:
            b = SubwayStop(station=station[0], route=route[0])
            b.save()
        except IntegrityError:
            pass

def create_tram_station(osmid, tags, coord):
    position = 'POINT({} {})'.format(coord[0], coord[1])
    b = TramStation(osmid=osmid, position=position)

    try:
        b.name = tags['name']
    except KeyError:
        pass

    b.save()

def create_tram_route(osmid, tags, members):
    """A tram route is in double in database, one per direction
    """
    b = TramRoute(osmid=osmid)

    try:
        b.name = tags['name']
    except KeyError:
        pass

    try:
        operator = tags['operator']
        b.operator = operator[:50]
    except KeyError:
        pass

    try:
        b.colour = tags['colour']
        if len(b.colour) > 10:
            b.colour = b.colour[:10]
    except KeyError:
        pass

    try:
        b.ref = tags['ref']
        if len(b.ref) > 10:
            b.ref = b.ref[:10]
    except KeyError:
        pass
    b.save()

def create_tram_stop(route_id, station_id):
    """A tram route is in double in database, one per direction
    """
    station = TramStation.objects.filter(osmid=station_id)
    route = TramRoute.objects.filter(osmid=route_id)

    if (len(station) == 1 and len(route) == 1):
        try:
            b = TramStop(station=station[0], route=route[0])
            b.save()
        except IntegrityError:
            pass

def create_bus_stop(osmid, tags, coord):
    position = 'POINT({} {})'.format(coord[0], coord[1])
    b = BusStop(osmid=osmid, position=position)

    try:
        b.name = tags['name']
    except KeyError:
        pass

    b.save()

def create_bus_route(osmid, tags, members):
    """A bus route is in double in database, one per direction
    """
    b = BusRoute(osmid=osmid)

    try:
        name = tags['name']
        b.name = name[:100]
    except KeyError:
        pass

    try:
        operator = tags['operator']
        b.operator = operator[:50]
    except KeyError:
        pass

    try:
        if tags['wheelchair'] == 'yes':
            b.wheelchair = True
    except KeyError:
        pass

    try:
        b.colour = tags['colour']
        if len(b.colour) > 10:
            b.colour = b.colour[:10]
    except KeyError:
        pass

    try:
        b.ref = tags['ref']
        if len(b.ref) > 10:
            b.ref = b.ref[:10]
    except KeyError:
        pass
    b.save()

def create_busroute_stop(route_id, stop_id):
    """A bus route is in double in database, one per direction
    """
    stop = BusStop.objects.filter(osmid=stop_id)
    route = BusRoute.objects.filter(osmid=route_id)

    if (len(stop) == 1 and len(route) == 1):
        try:
            b = BusRouteStop(stop=stop[0], route=route[0])
            b.save()
        except:
            pass

