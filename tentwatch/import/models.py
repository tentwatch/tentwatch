from django.db import models

class OtherTent(models.Model):
    title = models.CharField(max_length=140)
    url = models.URLField(max_length=1024)

    def __unicode__(self):
        return self.title
