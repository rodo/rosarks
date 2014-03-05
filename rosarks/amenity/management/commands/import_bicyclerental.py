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
from rosarks.amenity.models import BicycleRental, BusStop, SubwayStation

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
        p = OSMParser(concurrency=4, nodes_callback=chker.nodes)

        # Read filename on cmd arg
        p.parse(fpath)


class RosaParse(object):

    def nodes(self, nodes):
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


def create_bicycle_rental(osmid, tags, coord):
    position = 'POINT({} {})'.format(coord[0], coord[1])
    b = BicycleRental(osmid=osmid, position=position)

    try:
        b.capacity = int(tags['capacity'])
    except:
        pass

    try:
        b.operator = tags['operator']
    except KeyError:
        pass

    try:
        b.name = tags['name']
    except KeyError:
        pass

    b.save()

def create_bus_stop(osmid, tags, coord):
    position = 'POINT({} {})'.format(coord[0], coord[1])
    b = BusStop(osmid=osmid, position=position)

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
