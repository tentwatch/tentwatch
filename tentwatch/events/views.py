from datetime import datetime


from django.conf import settings
from django.shortcuts import get_object_or_404

from sleepy.base import Base
from sleepy.decorators import RequiresParameters
from sleepy.responses import api_out

from models import Event, parse_time
from tentwatch.categories.models import Category, ParentCategory

class EventsHandler(Base):

    def GET(
        self,
        request,
        id=None,
        start_time=None,
        end_time=None,
        category=None,
        parent_category=None,
        *args,
        **kwargs
        ):

        base = Event.objects

        if None != parent_category:
            base = base.filter(category__parent_category__name__exact=parent_category)

        if None != start_time:
            base = base.filter(time__gte=parse_time(start_time))

        if None != end_time:
            base = base.filter(time__lte=parse_time(end_time))

        if None != category:
            base = base.filter(category__name__exact=category)

        events = base.all()
        return api_out(
            [
                event.as_dict()
                for event
                in events
                ]
            )
        
    @RequiresParameters(["parent_category", "category", "lat", "lon"])
    def POST(self, request, parent_category, category, lat, lon, *args, **kwargs):
        try:
            parent_category = ParentCategory.objects.get(name=parent_category)
            category = Category.objects.get(name=category, parent_category=parent_category)
        except ParentCategory.DoesNotExist:
            return api_error("A parent category named {0} does not exist".format(parent_category))
        except Category.DoesNotExist:
            return api_error("A category named {0} does not exist".format(category))

        event = Event.objects.create(
            category=category,
            lat=float(lat),
            lon=float(lon),
            creator_ip=request.META["REMOTE_ADDR"]
            )

        return api_out(event.as_dict())
