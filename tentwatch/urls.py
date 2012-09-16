from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.shortcuts import render_to_response
admin.autodiscover()

from events.views import EventsHandler
from categories.views import CategoriesHandler, ParentCategoriesHandler

urlpatterns = patterns(
    '',
    url(r'^$', lambda request: render_to_response("index.html", {})),
    url(r'^events', EventsHandler(), name="event"),
    url(r'^categories/(?P<id>\d*?)', CategoriesHandler(), name="category"),
    url(r'^parent-categories/(?P<id>\d*?)', ParentCategoriesHandler(), name="parent-category"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
