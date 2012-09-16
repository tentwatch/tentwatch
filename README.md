Tent Watch
==========

A platform for informing other members in your local community about important events pertaining to natural disasters, crime, or community engagement.

Inception
=========

Tent Watch was initially created in Chattanooga, Tennessee during Hackanooga 2012.

Contributors
------------

  - Alex Ogle (Guy off the street)
  - Jason Volpe (Human 2.0)
  - Adam Haney (Handsome Gentlemen)
  - Micah Hausler (British Fellow)
  - Tony Cain (Design Adonis)

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


Licensing
=========

Source Code
-----------

Source code licensing is described in LICENSE.txt which should have been provided with this README. As of this writing it was GPLv3.

Data
----

We license our data using [Creative Commons Attribution license v 3.0](http://creativecommons.org/licenses/by/3.0/legalcode) and we suggest that any installations of Tent Watch use the same license to maximize the power and interoperability of tents in the community.
