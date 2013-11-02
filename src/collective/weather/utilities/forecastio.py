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
    """

    implements(IWeatherInfo)

    def getWeatherInfo(self, key, location, units='F', lang=None):
        """location must be a tuplish (lat, lang)
           unfortunately lang is not configurable for forecast.io
        """
        BASE_URL = 'https://api.forecast.io/forecast/{0}/{1},{2}?' \
                   'units={3}&exclude=minutely,hourly,daily,alerts,flags'

        BASE_ICON_URL = '++resource++collective.weather/{0}-icon.png'

        if key.strip() == '':
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

        response = urllib2.urlopen(BASE_URL.format(key, lat, long, units))
        forecast_info = json.loads(response.read())
        if 'currently' in forecast_info:
            forecast_info = forecast_info['currently']
        else:
            # TODO: Give a friendly message
            return None

        weather_info = {}
        weather_info['temperature'] = forecast_info['temperature']
        weather_info['summary'] = forecast_info['summary']
        weather_info['icon'] = BASE_ICON_URL.format(forecast_info['icon'])

        return weather_info
