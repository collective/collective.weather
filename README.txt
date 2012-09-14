******************
collective.weather
******************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A Plone viewlet to display the weather at selected locations.

Package supports `Yahoo! Weather`_, `Google`_ Weather and `NOAA`_'s `National
Weather Service`_.

Don't Panic
-----------

Go to Plone's control panel and open Weather Setup.

Select the service you want to use and the list of location ids that are going
to be available on the viewlet.

The user will be able to select from one of those locations. This information
will be stored inside a browser cookie.

The current weather condition of the selected location will be displayed at
the viewlet.

.. figure:: https://raw.github.com/collective/collective.weather/master/viewlet.png
    :align: center
    :height: 140px
    :width: 321px

    The Weather viewlet.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.weather.png
    :target: http://travis-ci.org/collective/collective.weather

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

Current Status
--------------

At this moment, `Yahoo! Weather`_ is the only service currently working.
As per 2012/09/14 `Google`_ Weather has stopped working and `NOAA`_'s `National Weather Service`_
is not currently implemented.

Yahoo Weather
-------------

In order to load locations to be used with the Yahoo! Weather service, you need to enter each one in the following format:

id|name|location_id

Where "id" should be a unique value and not repeated between any of the cities.
"name" is the name to be shown in the drop down, this doesn't need to be unique.
"location_id" is the id used by `Yahoo! Weather`_ to get the forecast information.

To know the location id for specific places, go to that location in `Yahoo! Weather`_ and the location id is part of the url.
For example, in the case of "Los Angeles" (http://weather.yahoo.com/forecast/USCA0638.html) the location id would be "USCA0638"



.. _`opening a support ticket`: https://github.com/collective/collective.weather/issues
.. _`Yahoo! Weather`: http://weather.yahoo.com/
.. _`Google`: http://www.google.com/
.. _`NOAA`: http://www.noaa.gov/
.. _`National Weather Service`: http://www.weather.gov/

