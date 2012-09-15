from sleepy.decorators import AbsolutePermalink

from django.db import models
from django.conf import settings
from tentwatch.categories.models import Category

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
        
        
        
