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
    osmid = models.IntegerField()

    name = models.CharField(max_length=100,
                            verbose_name='Name',
                            blank=True,
                            null=True)

    position = models.PointField()

    operator = models.CharField(max_length=30,
                                verbose_name='Operator',
                                blank=True,
                                null=True)

    capacity = models.IntegerField(blank=True,
                                   null=True)

    tags = models.CharField(max_length=3000,
                            verbose_name='Tags')

    date_import = models.DateTimeField(auto_now_add=True)

    objects = models.GeoManager()

    def __unicode__(self):
        """The unicode method
        """
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('line_detail', args=[str(self.id)])
