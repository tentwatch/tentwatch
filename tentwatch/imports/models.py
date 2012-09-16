from django.db import models

class OtherTent(models.Model):
    name = models.CharField(max_length=140)
    url = models.URLField(max_length=1024)
    lat = models.FloatField(default=0.0, editable=False)
    lon = models.FloatField(default=0.0, editable=False)

    def __unicode__(self):
        return self.name
