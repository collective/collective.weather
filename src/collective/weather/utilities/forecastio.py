# -*- coding: utf-8 -*-

###################################################################
#
# forecast.io API documentation
# https://developer.forecast.io/docs/v2
#
# Create a free account and you'll get an api key
# https://developer.forecast.io/register
#
###################################################################

try:
    import json
except ImportError:
    import simplejson as json

import logging

from collective.weather.config import PROJECTNAME
from collective.weather.interfaces import IWeatherInfo
from urllib2 import HTTPError
from urllib2 import urlopen
from zope.interface import implements

logger = logging.getLogger(PROJECTNAME)


class ForecastIO(object):
    """forecast.io implementation of IWeatherInfo

    >>> from zope.component import getUtility
    >>> from collective.weather.interfaces import IWeatherInfo

    Modify logger output for testing purposes

    >>> import sys, logging
    >>> root_logger = logging.getLogger()
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    >>> handler.setFormatter(formatter)
    >>> root_logger.addHandler(handler)


    Get the utility

    >>> utility = getUtility(IWeatherInfo, name='forecast.io')

    Test the utility with a blank key (log output)

    >>> forecastio = utility('')
    >>> forecastio.getWeatherInfo('25,20')
    collective.weather - WARNING - Missing forecast.io api key

    Initialize the utility with the provider's key

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
    >>> info = forecastio.getWeatherInfo(lat_lang, units='metric')
    >>> '%.2f' % info['temperature']  # For Python 2.6
    '18.84'
    >>> info['summary']
    'Sunny'
    >>> info['icon']
    'sunny-icon.png'

    Test with a lat_lang string and a different unit

    >>> info = forecastio.getWeatherInfo('25,20', units='imperial')
    >>> '%.2f' % info['temperature']  # For Python 2.6
    '65.91'

    Test a non lat_lang location (log output)

    >>> info = forecastio.getWeatherInfo('Buenos Aires')
    collective.weather - WARNING - Not a valid (lat, lang) location
    >>> info is None
    True

    Test a non existing (not registered) location (log output)

    >>> info = forecastio.getWeatherInfo('45,10', units='metric')
    collective.weather - WARNING - forecast.io returned no information for coordinates 45, 10
    >>> info
    {}
    """

    implements(IWeatherInfo)

    BASE_URL = 'https://api.forecast.io/forecast/{0}/{1},{2}?' \
               'units={3}&exclude=minutely,hourly,daily,alerts,flags'

    BASE_ICON_URL = '++resource++collective.weather.icons/{0}-icon.png'

    def __init__(self, key=None):
        self.key = key

    def _getWeatherInfo(self, lat, long, units):
        """Helper method to call the remote web service and
           to return a simple dictionary
        """

        url = self.BASE_URL
        icon_url = self.BASE_ICON_URL
        try:
            response = urlopen(url.format(self.key, lat, long, units))
        except HTTPError, error:
            return {'error': error.code, 'text': error.reason}

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

    def getWeatherInfo(self, location, units='metric', lang='en'):
        """location must be a tuplish (lat, lang)
           unfortunately lang is not configurable for forecast.io
        """

        if self.key.strip() == '':
            logger.warning(u'Missing forecast.io api key')
            return None

        if isinstance(location, basestring):
            location = location.split(',')

        if isinstance(location, (list, tuple)):
            try:
                lat, long = location
            except ValueError:  # Too many values to unpack
                logger.warning('Not a valid (lat, lang) location')
                return None
        else:
            logger.warning('Not a valid (lat, lang) location')
            return None

        if units == 'metric':
            units = 'si'
        else:
            units = 'us'

        weather_info = self._getWeatherInfo(lat, long, units)

        if 'error' in weather_info:
            warning = 'forecast.io api returned this {0} error: {1}'
            logger.warning(warning.format(weather_info['error'],
                                          weather_info['text']))
        elif weather_info == {}:
            warning = 'forecast.io returned no information for coordinates {0}, {1}'
            logger.warning(warning.format(lat, long))

        return weather_info
