******************
collective.weather
******************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A Plone viewlet to display the weather at selected locations.

Current Status
^^^^^^^^^^^^^^

Currently, `Yahoo! Weather`_ is the only service working. As per 2012/09/14
`Google`_ Weather has stopped working and `NOAA`_'s `National Weather
Service`_ has not being implemented yet.

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

Yahoo Weather
^^^^^^^^^^^^^

In order to load locations to be used with the Yahoo! Weather service, you
need to enter each one in the following format:

id|name|location_id

Where *id* should be a unique value and not repeated among any of the cities;
*name* is the name to be shown in the drop down, this doesn't need to be
unique; *location_id* is the id used by `Yahoo! Weather`_ to get the forecast
information.

To know the location id for specific places, go to `The Weather Channel`_,
search for that location and get the id from the url.

For example, in the case of `Caracas, Venezuela`_, the location id would be
**VEXX0008**; for `Beijing, China`_ it would be **CHXX0008**, and for `Los
Angeles, CA`_ it would be **USCA0638**.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.weather.png
    :target: http://travis-ci.org/collective/collective.weather

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.weather/issues
.. _`Yahoo! Weather`: http://weather.yahoo.com/
.. _`Google`: http://www.google.com/
.. _`NOAA`: http://www.noaa.gov/
.. _`National Weather Service`: http://www.weather.gov/
.. _`The Weather Channel`: http://www.weather.com/
.. _`Caracas, Venezuela`: http://www.weather.com/weather/right-now/Caracas+Venezuela+VEXX0008
.. _`Beijing, China`: http://www.weather.com/weather/right-now/CHXX0008:1
.. _`Los Angeles, CA`: http://www.weather.com/weather/right-now/Los+Angeles+CA+USCA0638
