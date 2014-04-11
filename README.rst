******************
collective.weather
******************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

A Plone package to display the current weather at selected locations inside a
portlet or viewlet.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.weather.png?branch=master
    :target: http://travis-ci.org/collective/collective.weather

.. image:: https://coveralls.io/repos/collective/collective.weather/badge.png?branch=master
    :target: https://coveralls.io/r/collective/collective.weather

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this package on a buildout-based installation:

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
        https://good-py.appspot.com/release/dexterity/1.2.1?plone=4.1.6

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ''collective.weather'' and click the 'Activate' button.

.. Note::
    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.

Usage
^^^^^

Go to Site Setup and select 'Weather'.

Enter the list of locations that are going to be available on the site in the
following format::

    location_id|name

Where *location_id* should be a unique value and not repeated among any of the
locations; *name* is the name to be shown in the drop down (this doesn't need
to be unique). Some examples could be::

    455827|São Paulo (for Yahoo! Weather)
    -23.548871,-46.638814|São Paulo (for Forecast.io and Weather Underground)

Select the sistem of units: Metric or Imperial. Metric system uses degrees
Celsius. Imperial system uses degrees Fahrenheit.

Finding locations
^^^^^^^^^^^^^^^^^

Different weather service providers need different location ids to get
weather conditions.

You'll have to change the **Available locations** setting depending on your
selection. Please, refer to providers documentation for more information:

- `Yahoo Weather`_ needs a `WOEID`_. There's a convenient `online tool to
  get WOEID`_.
- `Forecast.io API`_ just needs a ``latitude, longitude`` coordinate.
- `Weather Underground`_ accepts many options (check the ``query`` option).

Portlet
^^^^^^^

The package includes a portlet that you can add in your site.

- Open the 'Manage portlets' screen and select 'Weather portlet'
- Set the title of the portlet
- Select a city from the list

.. image:: https://raw.github.com/collective/collective.weather/master/portlet.png
    :align: center
    :alt: The Weather portlet

Viewlet
^^^^^^^

.. Warning::
    The weather viewlet, as originaly planned, has proven to be pretty complex
    to implement. Current implementation is still buggy. Use it at your own
    risk.

The package also includes a viewlet that will display the weather in one of
the locations defined in the settings. The viewlet will be displayed on top of
the site inside the IPortalHeader viewlet manager.

To use the viewlet you need to activate it: go to Site Setup and select
'Weather' again. Select the 'Show weather viewlet?' box.

The user will be able to select from one of the locations (this information
will be stored inside a cookie to show this location the next time the user
visits the site).

The current weather condition of the selected location will be displayed at
the viewlet.

.. image:: https://raw.github.com/collective/collective.weather/master/viewlet.png
    :align: center
    :alt: The Weather viewlet

Internals
+++++++++

.. Note::
    This section could be outdated.

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

Extending the package with new weather providers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In case you want to contribute with new weather providers for this package or
if you want to add a new one in a custom package for your site you'll just
need to create a new named utility that should implement
``collective.weather.interfaces.IWeatherInfo``.

**Weather** control panel will automatically learn about the new utility and
it will be listed as an option in the provider's drop-down.

This package already comes with some utilities you can check to get a quick
idea of how to create yours:

- `yahoo <https://github.com/collective/collective.weather/blob/master/src/collective/weather/utilities/yahoo.py>`_
- `forecast.io <https://github.com/collective/collective.weather/blob/master/src/collective/weather/utilities/forecastio.py>`_
- `wunderground <https://github.com/collective/collective.weather/blob/master/src/collective/weather/utilities/wunderground.pyweather>`_

`The API for this utility`_ is very simple.

In case your utility needs `an API key you can pass it on initialization`_.

Here's and example you can copy and paste to start your custom utility::

    """Example of a named utility for IWeatherInfo.
    """
    from collective.weather.interfaces import IWeatherInfo
    from zope.interface import implements


    class DummyProvider(object):
        """Dummy weather implementation of IWeatherInfo
        """
        implements(IWeatherInfo)

        def __init__(self, key=None):
            self.key = key

        def getWeatherInfo(self, location, units='metric', lang='en'):
            """Dummy implementation of getWeatherInfo as an example
            """
            return {
                'summary': u'What a lovely day!',
                'temperature': 20,
                'icon': u'lovely-day-icon.png',
            }

Not entirely unlike
-------------------

`Weather Forecast`_
    A very old an unmaintained product, Weather Forecast is a portlet that
    will display the observation of the weather. Compatible with Plone 2.5.

.. _`Forecast.io API`: https://developer.forecast.io/docs/v2
.. _`online tool to get WOEID`: http://woeid.rosselliot.co.nz/lookup
.. _`opening a support ticket`: https://github.com/collective/collective.weather/issues
.. _`Weather Forecast`: http://plone.org/products/ploneweatherforecast
.. _`Yahoo Weather`: http://developer.yahoo.com/weather/
.. _`Yahoo! Weather`: http://weather.yahoo.com/
.. _an API key you can pass it on initialization: https://github.com/collective/collective.weather/blob/master/src/collective/weather/utilities/forecastio.py#L114
.. _The API for this utility: https://github.com/collective/collective.weather/blob/master/src/collective/weather/interfaces.py#L21
.. _Weather Underground: http://www.wunderground.com/weather/api/d/docs?d=data/index&MR=1
.. _WOEID: http://developer.yahoo.com/geo/geoplanet/guide/concepts.html#woeids
