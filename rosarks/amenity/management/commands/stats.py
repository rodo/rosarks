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
Purge all datas
"""
from django.core.management.base import BaseCommand
from rosarks.amenity.models import BicycleRental, BusStop, BusRoute
from rosarks.amenity.models import SubwayStation, SubwayRoute, SubwayStop
from rosarks.amenity.models import TramStation, TramRoute, TramStop


class Command(BaseCommand):
    help = 'Import data in file [ARG]'

    def handle(self, *args, **options):
        """
        Handle the munin command
        """
        print "bicycle_rental : %s" % (BicycleRental.objects.all().count())
        print "bus stop : %s" % (BusStop.objects.all().count())
        print "bus route : %s" % (BusRoute.objects.all().count())
        print "subway station : %s" % (SubwayStation.objects.all().count())
        print "subway route   : %s " % (SubwayRoute.objects.all().count())
        print "subway stops   : %s" % (SubwayStop.objects.all().count())
        print "tram station : %s" % (TramStation.objects.all().count())
        print "tram route   : %s " % (TramRoute.objects.all().count())
        print "tram stops   : %s "% (TramStop.objects.all().count())
