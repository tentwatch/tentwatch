"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json

from django.test import TestCase, Client
from tentwatch.categories.models import Category, ParentCategory

class EventCreationTest(TestCase):
    def setUp(self):
        self.client = Client()
        parent_category = ParentCategory.objects.create(name="Criminal Activity")
        Category.objects.create(name="Shooting", parent_category=parent_category)

        self.event_response = self.client.post(
                "/events/",
                {
                    "parent_category": "Criminal Activity",
                    "category": "Shooting",
                    "lat": 57.42,
                    "lon": 42.44
                    }
                )
        self.event_response_dict = json.loads(self.event_response.content)

    def test_event_creation(self):
        assert self.event_response.status_code == 200

    def test_event_creation_long(self):
        assert float(self.event_response_dict["data"]["location"]["long"]) == 42.44

    def test_event_creation_lat(self):
        assert float(self.event_response_dict["data"]["location"]["lat"]) == 57.42

    def test_event_creation_parent_category(self):
        assert self.event_response_dict["data"]["category"]["parent"]["name"] == "Criminal Activity"

    def test_event_creation_parent_category(self):
        assert self.event_response_dict["data"]["category"]["name"] == "Shooting"
    
        
