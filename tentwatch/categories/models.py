from sleepy.decorators import AbsolutePermalink

from django.db import models

class ParentCategory(models.Model):
    name = models.CharField(max_length=32)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Parent Categories"

    def __unicode__(self):
        return self.name


    def as_dict(self):
        return {
            "name": self.name,
            "link": self.get_absolute_url()
            }

    @AbsolutePermalink
    def get_absolute_url(self):
        return ('parent-category', [self.id])

class Category(models.Model):
    name = models.CharField(max_length=32)
    parent_category = models.ForeignKey(ParentCategory, related_name='children')
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return u"{0}:{1}".format(
            unicode(self.parent_category),
            self.name
            )

    def as_dict(self):
        return {
            "name": self.name,
            "link": self.get_absolute_url(),
            "parent": self.parent_category.as_dict()
            }

    @AbsolutePermalink
    def get_absolute_url(self):
        return ('category', [self.id])
            
