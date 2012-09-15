import requests

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Pulls events that happened on other tent watch installations into this installation"
    args = "<tentwatch-api-url>"

    def handle(self, *args, **options):
        try:
            endpoint = args[0]
        except IndexError:
            raise CommandError("You must enter an api endpoint")

        events = requests.get("{0}/events".format(endpoint)).json["data"]
        
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


        print parent_categories
        print categories

        for event in events:
            ev = Event.objects.create(
                category=categories_by_name[event["category"]["name"]]
                parent_category=parent_categories_by_name[event["category"]["parent"]["name"]],
                lat=event["lat"],
                long=event["long"],
                )
            ev.time = parse_time(event["created"])
            
        Event.objects.bulk_create(
            [
                for event
                in events
                ]
            )

                                     
        
