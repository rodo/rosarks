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
Models definition for resume
"""
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse


class BicycleRental(models.Model):
    """
    Bicycle rental service
    """
    osmid = models.BigIntegerField(unique=True)

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)

    # Auto index is buggy in GeoDjango 1.4
    position = models.PointField(spatial_index=False)

    operator = models.CharField(max_length=50,
                                verbose_name='Operator',
                                blank=True,
                                null=True)

    capacity = models.IntegerField(blank=True,
                                   null=True)

    date_import = models.DateTimeField(auto_now_add=True)

    objects = models.GeoManager()

    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)


class BusStop(models.Model):
    """
    Where the bus stop and take passenger
    """
    osmid = models.BigIntegerField(unique=True)

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)

    position = models.PointField(spatial_index=False)

    date_import = models.DateTimeField(auto_now_add=True)

    objects = models.GeoManager()

    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)


class BusRoute(models.Model):
    """
    Where the bus stop and take passenger
    """
    osmid = models.BigIntegerField(unique=True)

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)

    ref = models.CharField(max_length=10, blank=True, null=True)
    colour = models.CharField(max_length=10, blank=True, null=True)

    operator = models.CharField(max_length=50,
                                verbose_name='Operator',
                                blank=True,
                                null=True)

    date_import = models.DateTimeField(auto_now_add=True)

    wheelchair = models.BooleanField(default=False)

    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)


class BusRouteStop(models.Model):
    """
    A bus stop
    """
    route = models.ForeignKey(BusRoute)
    stop = models.ForeignKey(BusStop)


class SubwayStation(models.Model):
    """
    Subway Station
    """
    osmid = models.BigIntegerField(unique=True)

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)

    position = models.PointField(spatial_index=False)

    date_import = models.DateTimeField(auto_now_add=True)

    objects = models.GeoManager()

    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)


class SubwayRoute(models.Model):
    """
    Subway Route
    """
    osmid = models.BigIntegerField(unique=True)

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)    

    ref = models.CharField(max_length=10, blank=True, null=True)
    colour = models.CharField(max_length=10, blank=True, null=True)
    date_import = models.DateTimeField(auto_now_add=True)

    operator = models.CharField(max_length=50,
                                verbose_name='Operator',
                                blank=True,
                                null=True)

    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)


class SubwayStop(models.Model):
    """
    A subway stop
    """
    route = models.ForeignKey(SubwayRoute)
    station = models.ForeignKey(SubwayStation)

    class Meta:
        unique_together = ('route', 'station',)


class TramStation(models.Model):
    """
    Tram Station
    """
    osmid = models.BigIntegerField(unique=True)

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)

    position = models.PointField(spatial_index=False)

    date_import = models.DateTimeField(auto_now_add=True)

    objects = models.GeoManager()

    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)


class TramRoute(models.Model):
    """
    Tram Route
    """
    osmid = models.BigIntegerField(unique=True)

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)

    ref = models.CharField(max_length=10, blank=True, null=True)
    colour = models.CharField(max_length=10, blank=True, null=True)

    operator = models.CharField(max_length=50,
                                verbose_name='Operator',
                                blank=True,
                                null=True)

    date_import = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)


class TramStop(models.Model):
    """
    A tram stop
    """
    route = models.ForeignKey(TramRoute)
    station = models.ForeignKey(TramStation)

    class Meta:
        unique_together = ('route', 'station',)
