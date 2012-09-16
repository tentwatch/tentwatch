Tent Watch
==========

A platform for informing other members in your local community about important events pertaining to natural disasters, crime, or community engagement.

Inception
=========

Tent Watch was initially created in Chattanooga, Tennessee during Hackanooga 2012.


Installation
============

Debian/Ubuntu
-------------
    $ sudo apt-get -y install nginx-extras python-virtualenv python-dev
    $ sudo pip install uwsgi

    In the repository 
    $ virutalenve venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt

API Cheat Sheet
===============

Creating Events
---------------

    # POST an event with a parent_category (string), category (string), lat (float), and lon(float)
    curl -X POST http://tentwatch.com/events?parent_category=Crime&category=Shooting&lat=37.45&lon=33.44