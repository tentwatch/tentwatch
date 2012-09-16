import requests

from tentwatch.imports.models import OtherTent
from django.core.management.base import BaseCommand, CommandError

class Unreachable(Exception):
    pass

class Command(BaseCommand):
    help = "Pulls events that happened on other tent watch installations into this installation"
    args = "<tentwatch-api-url>"

    def crawl_tent(self, tent):
        try:
            events = requests.get("{0}/events".format(tent.url)).json["data"]
        except TypeError:
            raise Unreachable
        
        parent_categories = list(
            set(
                [
                    event["category"]["parent"]["name"]
                    for event
                    in events
                    ]
                )
            )

        parent_categories_by_name = {}
        for cat in parent_categories:
            obj, news = ParentCategory.objects.get_or_create(
                name=cat
                )

            if new:
                obj.visible = False
                obj.save()

            parent_categories_by_name[cat] = obj

        categories = list(
            set(
                [
                    event["category"]["parent"]["name"]
                    for event
                    in events
                    ]
                )
            )

        categories_by_name = {}
        for cat in categories:
            obj, new = Category.objects.get_or_create(
                name=cat
                )

            if new:
                obj.visible = False
                obj.save()

            categories_by_name[cat] = obj

        for event in events:
            ev = Event.objects.create(
                category=categories_by_name[event["category"]["name"]],
                parent_category=parent_categories_by_name[event["category"]["parent"]["name"]],
                lat=event["lat"],
                long=event["lon"],
                )
            ev.time = parse_time(event["created"])


    def handle(self, *args, **options):
        for tent in OtherTent.objects.all():
            try:
                self.crawl_tent(tent)
                print "Success: {0}".format(tent.name)
            except Unreachable:
                print "Failed: {0}, unreachable".format(tent.name)
            except Exception, e:
                print "Failed: {0} {1}".format(tent.name, e)


                                     
        
