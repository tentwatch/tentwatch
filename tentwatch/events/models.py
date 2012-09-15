from sleepy.decorators import AbsolutePermalink

import pytz
from django.utils.timezone import utc

from django.db import models
from django.conf import settings
from tentwatch.categories.models import Category

def parse_time(self, time_string):
    time_string = datetime.strptime(time_string, settings.TIME_FORMAT)
    time_string.replace(tzinfo=utc)
    return pytz.UTC.localize(time_string)


class Event(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lon = models.FloatField()
    category = models.ForeignKey(Category)
    creator_ip = models.IPAddressField()

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return u"{0} at {1}, {2}".format(
            unicode(self.category),
            self.lat,
            self.lon
            )

    def as_dict(self):
        return {
            "created": self.time.strftime(settings.TIME_FORMAT),
            "location": {
                "lat": self.lat,
                "long": self.lon
                },
            "category": self.category.as_dict(),
            "link": self.get_absolute_url(),
            "id": self.pk
            }

    @AbsolutePermalink
    def get_absolute_url(self):
        return ('event', [self.id])
        
        
        
