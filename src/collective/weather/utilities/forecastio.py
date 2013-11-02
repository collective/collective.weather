# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    import simplejson as json
import urllib2

from zope.interface import implements
from collective.weather.interfaces import IWeatherInfo


class ForecastIO(object):
    """forecast.io implementation of IWeatherInfo

    >>> from zope.component import getUtility
    >>> from collective.weather.interfaces import IWeatherInfo

    Get the utility

    >>> utility = getUtility(IWeatherInfo, name='forecastio')

    And initialize it with the provider's key

    >>> key = 'my-secret-key'
    >>> forecastio = utility(key)
    >>> forecastio.key
    'my-secret-key'

    Monkey patch _getWeatherInfo to avoid actual web service call



    >>> def _getWeatherInfo(lat, long, units):
    ...    weather_infos = {
    ...        '25,20,si': {'temperature': 18.84,
    ...                     'summary': 'Sunny',
    ...                     'icon': 'sunny-icon.png'},
    ...        '25,20,us': {'temperature': 65.91,
    ...                     'summary': 'Sunny',
    ...                     'icon': 'sunny-icon.png'}
    ...    }
    ...    key = '{0},{1},{2}'.format(lat, long, units)
    ...    if key in weather_infos:
    ...        return weather_infos[key]
    ...    else:
    ...        return {}

    >>> forecastio._getWeatherInfo = _getWeatherInfo

    Test with a lat_lang as a tuple

    >>> lat_lang = (25, 20,)
    >>> info = forecastio.getWeatherInfo(lat_lang, units='C')
    >>> info['temperature']
    18.84
    >>> info['summary']
    'Sunny'
    >>> info['icon']
    'sunny-icon.png'

    Test with a lat_lang string and a different unit

    >>> info = forecastio.getWeatherInfo('25,20', units='F')
    >>> info['temperature']
    65.91

    Test a non lat_lang location

    >>> info = forecastio.getWeatherInfo('Buenos Aires')
    >>> info is None
    True

    Test a non existing (not registered) location

    >>> info = forecastio.getWeatherInfo('45,10', units='C')
    >>> info
    {}
    """

    implements(IWeatherInfo)

    BASE_URL = 'https://api.forecast.io/forecast/{0}/{1},{2}?' \
               'units={3}&exclude=minutely,hourly,daily,alerts,flags'

    BASE_ICON_URL = '++resource++collective.weather/{0}-icon.png'

    def __init__(self, key=None):
        self.key = key

    def _getWeatherInfo(self, lat, long, units):
        """Helper method to call the remote web service and
           to return a simple dictionary
        """

        url = self.BASE_URL
        icon_url = self.BASE_ICON_URL
        response = urllib2.urlopen(url.format(self.key, lat, long, units))
        forecast_info = json.loads(response.read())
        if 'currently' in forecast_info:
            forecast_info = forecast_info['currently']
        else:
            forecast_info = {}

        weather_info = {}
        if 'temperature' in forecast_info and \
           'summary' in forecast_info and \
           'icon' in forecast_info:
            weather_info = {}
            weather_info['temperature'] = forecast_info['temperature']
            weather_info['summary'] = forecast_info['summary']
            weather_info['icon'] = icon_url.format(forecast_info['icon'])

        return weather_info

    def getWeatherInfo(self, location, units='F', lang=None):
        """location must be a tuplish (lat, lang)
           unfortunately lang is not configurable for forecast.io
        """

        if self.key.strip() == '':
            # TODO: Give a friendly message
            return None

        if isinstance(location, basestring):
            location = location.split(',')

        if isinstance(location, (list, tuple)):
            try:
                lat, long = location
            except ValueError:  # Too many values to unpack
                # TODO: Give a friendly message
                return None
        else:
            # TODO: Give a friendly message
            return None

        if units == 'C':
            units = 'si'
        else:
            units = 'us'

        weather_info = self._getWeatherInfo(lat, long, units)

        return weather_info
