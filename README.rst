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

Select the weather service to be used (currently only Yahoo! Weather is
supported).

Enter the list of locations that are going to be available on the site in the
following format::

    id|name|location_id

Where *id* should be a unique value and not repeated among any of the
locations; *name* is the name to be shown in the drop down (this doesn't need
to be unique); *location_id* is the id used by `The Weather Channel`_ to get
the forecast information (see below how to find these ids).

Select the sistem of units: Metric or Imperial. Metric system uses degrees
Celsius. Imperial system uses degrees Fahrenheit.

Finding locations
^^^^^^^^^^^^^^^^^

Finding out locations is currently the most difficult part of using this
package. First, you have to make a search like this in your favorite web
search engine::

    joao pessoa brazil weather

.. image:: https://raw.github.com/collective/collective.weather/master/search.png
    :align: center
    :alt: Searching for a location

Then, you will have identify the *location_id* on the URL (BRXX0128 in this
case)::

    http://www.weather.com/weather/today/Joao+Pessoa+Brazil+BRXX0128

Other examples:

* `Caracas, Venezuela`_: VEXX0008
* `Beijing, China`_: CHXX0008
* `Los Angeles, CA`_: USCA0638

Portlet
^^^^^^^

The package includes a portlet that you can add in your site.

* Open the 'Manage portlets' screen and select 'Weather portlet'
* Set the title of the portlet
* Select a city from the list

.. image:: https://raw.github.com/collective/collective.weather/master/portlet.png
    :align: center
    :alt: The Weather portlet

Viewlet
^^^^^^^

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

Not entirely unlike
-------------------

`Weather Forecast`_
    A very old an unmaintained product, Weather Forecast is a portlet that
    will display the observation of the weather. Compatible with Plone 2.5.

.. _`Beijing, China`: http://www.weather.com/weather/today/Beijing+China+CHXX0008
.. _`Caracas, Venezuela`: http://www.weather.com/weather/today/Caracas+Venezuela+VEXX0008
.. _`Los Angeles, CA`: http://www.weather.com/weather/today/Los+Angeles+CA+USCA0638
.. _`opening a support ticket`: https://github.com/collective/collective.weather/issues
.. _`The Weather Channel`: http://www.weather.com/
.. _`Weather Forecast`: http://plone.org/products/ploneweatherforecast
.. _`Yahoo! Weather`: http://weather.yahoo.com/
