******************
collective.weather
******************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A Plone package to display the weather at selected locations.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.weather.png?branch=master
    :target: http://travis-ci.org/collective/collective.weather

.. image:: https://coveralls.io/repos/collective/collective.weather/badge.png?branch=master
    :target: https://coveralls.io/r/collective/collective.weather

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Current Status
^^^^^^^^^^^^^^

Currently, `Yahoo! Weather`_ is the only service working. As per 2012/09/14
`Google`_ Weather has stopped working and `NOAA`_'s `National Weather
Service`_ has not being implemented yet.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add ``collective.weather`` to the list of eggs
   to install::

    [buildout]
    ...
    eggs =
        collective.weather

#. If you are using Plone 4.1, you may need to extend a Dexterity known good
   set (KGS) to make sure that you get the right versions of the packages that
   make up Dexterity::

    [buildout]
    ...
    extends =
        http://good-py.appspot.com/release/dexterity/1.2.1

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ''collective.weather'' and click the 'Activate' button.

.. Note::
    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.

Usage
^^^^^

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

Internals
^^^^^^^^^

The weather viewlet uses Javascript in order to change cities, so this will
only work for Javascript enabled browsers.

To render the city weather, there is a "current-weather" view that will
render the latest info it has on weather conditions for a given city.
A cookie is used to get the latest chosen city, and you can override it
by passing a "city" argument to the view.

To update the city weather, there is a "update-weather", that, when called
without parameters, it will update all cities from the list.
You can pass a "city" argument to the view, to only update the given city.

There's an internal cache for each city (30 minutes), that if not enough
time has passed, then it will assume the current weather is updated, and
it will not do anything.

The Javascript that changes the city, will call this "update-weather" for
the chosen city to update it first. Thanks to this internal cache, this
view will return fast, if not enough time has passed.

In order to make it really fast for visitors of your site, you can set-up
a clockserver job to call this "update-weather" view with no params, once
every 30 minutes, so weather information for all your cities are ready for
when the visitor changes it from the drop-down.


.. _`opening a support ticket`: https://github.com/collective/collective.weather/issues
.. _`Yahoo! Weather`: http://weather.yahoo.com/
.. _`Google`: http://www.google.com/
.. _`NOAA`: http://www.noaa.gov/
.. _`National Weather Service`: http://www.weather.gov/
.. _`The Weather Channel`: http://www.weather.com/
.. _`Caracas, Venezuela`: http://www.weather.com/weather/right-now/Caracas+Venezuela+VEXX0008
.. _`Beijing, China`: http://www.weather.com/weather/right-now/CHXX0008:1
.. _`Los Angeles, CA`: http://www.weather.com/weather/right-now/Los+Angeles+CA+USCA0638
