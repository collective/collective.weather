# -*- coding: utf-8 -*-

""" forecast.io API documentation
    https://developer.forecast.io/docs/v2

    Create a free account and you'll get an api key
    https://developer.forecast.io/register
"""


from collective.weather.config import PROJECTNAME
from collective.weather.interfaces import IWeatherInfo
from urllib2 import HTTPError
from urllib2 import urlopen
from zope.interface import implements

import json
import logging

logger = logging.getLogger(PROJECTNAME)


class ForecastIO(object):
    """forecast.io implementation of IWeatherInfo
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
        if not self.key:
            msg = u'Missing Forecast.io API key'
            logger.warning(msg)
            raise ValueError(msg)

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
