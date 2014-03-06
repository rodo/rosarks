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
from rosarks.amenity.models import BicycleRental, BusStop
from rosarks.amenity.models import SubwayStation, SubwayRoute, SubwayStop

class Command(BaseCommand):
    help = 'Import data in file [ARG]'

    def handle(self, *args, **options):
        """
        Handle the munin command
        """
        print BicycleRental.objects.all().count()
        print BusStop.objects.all().count()
        print SubwayStation.objects.all().count()
        print SubwayRoute.objects.all().count()
        print SubwayStop.objects.all().count()
