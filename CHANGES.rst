Changelog
---------

There's a frood who really knows where his towel is.

1.0a4 (2014-04-11)
^^^^^^^^^^^^^^^^^^

.. Warning::
    This release includes many changes in the package structure and is not
    backwards compatible.

- Update package documentation.
  [marcosfromero, hvelarde]

- Weather viewlet is disabled as it is too buggy and is causing a lot of
  weird issues.
  [hvelarde]

- Refactor weather_utility to use location_id as key. (closes `#36`_).
  [marcosfromero]

- Depend on plone.api and remove dependency on pywapi.
  [hvelarde]

- New named utilities for Forecast.io and Weather Underground (closes `#18`_).
  [marcosfromero]

- New API for named utilities and Yahoo! Weather implementation.
  [marcosfromero]

- The weather portlet is now configurable.
  [marcosfromero]


1.0a3 (2013-10-29)
^^^^^^^^^^^^^^^^^^

.. Warning::
    This release includes many changes in the package structure and is not
    backwards compatible.

- Spanish and Brazilian Portuguese translations were updated. [hvelarde]

- Package documentation was updated. [hvelarde]

- A new option to define whether or not the weather viewlet is visible was
  added; by default the viewlet is hidden (closes `#14`_). [hvelarde]

- Control panel configlet was simplified; now all package settings are defined
  in one screen (closes `#19`_). [hvelarde]

- WeatherUtility is now registered as a global utility as we have no data to
  persist on it (closes `#7`_). If you're still stock with a
  ``TypeError: ('object.new(WeatherUtility) is not safe...``
  error, keep calm an read the section dedicated to **componentregistry.xml**
  on `How to make your Plone add-on products uninstall cleanly`_. May the
  Force be with you. [hvelarde]

- Add weather portlet that displays weather conditions of current city
  (closes `#9`_). [marcosfromero]

- Remove all Google Weather related code. [marcosfromero]

- Weather conditions moved to title tag. [flecox]


1.0a2 (2012-09-14)
^^^^^^^^^^^^^^^^^^

- Made the code to be more resistent to invalid data from the weather server.
  [frapell]

- Major refactoring to allow updates and city changes through AJAX calls
  (fixes `#6`_). [frapell]

- Implemented Yahoo! Weather. [frapell]


1.0a1 (2012-08-01)
^^^^^^^^^^^^^^^^^^

- Initial release.

.. _`#6`: https://github.com/collective/collective.weather/issues/6
.. _`#7`: https://github.com/collective/collective.weather/issues/7
.. _`#9`: https://github.com/collective/collective.weather/issues/9
.. _`#11`: https://github.com/collective/collective.weather/issues/11
.. _`#14`: https://github.com/collective/collective.weather/issues/14
.. _`#18`: https://github.com/collective/collective.weather/issues/18
.. _`#19`: https://github.com/collective/collective.weather/issues/19
.. _`#36`: https://github.com/collective/collective.weather/issues/36
.. _`How to make your Plone add-on products uninstall cleanly`: http://blog.keul.it/2013/05/how-to-make-your-plone-add-on-products.html
