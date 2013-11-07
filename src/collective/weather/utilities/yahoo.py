# -*- coding: utf-8 -*-

""" Yahoo! Weather api documentation
    http://developer.yahoo.com/weather/
"""

from collective.weather.config import PROJECTNAME
from collective.weather.interfaces import IWeatherInfo
from urllib2 import HTTPError
from urllib2 import urlopen
from xml.dom import minidom
from zope.interface import implements

import logging

logger = logging.getLogger(PROJECTNAME)


class Yahoo(object):
    """Yahoo weather implementation of IWeatherInfo

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

    >>> utility = getUtility(IWeatherInfo, name='yahoo')

    Test the utility with a blank key (log output)

    >>> yahoo = utility('')

    Monkey patch _getWeatherInfo to avoid actual web service call

    >>> def _getWeatherInfo(location, units):
    ...    weather_infos = {
    ...        '2502265,c': {'temperature': 18.0,
    ...                     'summary': 'Sunny',
    ...                     'icon': 'sunny-icon.png'},
    ...        '2502265,f': {'temperature': 65.0,
    ...                     'summary': 'Sunny',
    ...                     'icon': 'sunny-icon.png'}
    ...    }
    ...    key = '{0},{1}'.format(location, units)
    ...    if key in weather_infos:
    ...        return weather_infos[key]
    ...    else:
    ...        return {}

    >>> yahoo._getWeatherInfo = _getWeatherInfo

    Test with a known location

    >>> info = yahoo.getWeatherInfo('2502265', units='metric')
    >>> '%.2f' % info['temperature']  # For Python 2.6
    '18.00'
    >>> info['summary']
    'Sunny'
    >>> info['icon']
    'sunny-icon.png'

    Test with a different unit

    >>> info = yahoo.getWeatherInfo('2502265', units='imperial')
    >>> '%.2f' % info['temperature']  # For Python 2.6
    '65.00'

    Test with a unknown location (log output)
    >>> info = yahoo.getWeatherInfo('4444444')
    collective.weather - WARNING - Yahoo! weather api returned no information for location 4444444
    >>> info
    {}

    """

    implements(IWeatherInfo)

    BASE_URL = 'http://weather.yahooapis.com/forecastrss?w={0}&u={1}'

    BASE_ICON_URL = 'http://l.yimg.com/a/i/us/we/52/{0}.gif'

    def __init__(self, key=None):
        self.key = key

    def _getWeatherInfo(self, location, units):
        """Helper method to call the remote web service and
           to return a simple dictionary
        """

        url = self.BASE_URL
        icon_url = self.BASE_ICON_URL

        try:
            response = urlopen(url.format(location, units))
        except HTTPError, error:
            return {'error': error.code, 'text': error.reason}

        forecast_info = minidom.parseString(response.read())

        nodes = ['channel', 'item', 'yweather:condition']
        for node in nodes:
            forecast_info = forecast_info.getElementsByTagName(node)
            if len(forecast_info) == 1:
                forecast_info = forecast_info[0]
            else:
                forecast_info = None
                break

        weather_info = {}
        if forecast_info and \
           forecast_info.hasAttribute('temp') and \
           forecast_info.hasAttribute('text') and \
           forecast_info.hasAttribute('code'):
            weather_info = {}
            weather_info['temperature'] = float(forecast_info.getAttribute('temp'))
            weather_info['summary'] = forecast_info.getAttribute('text')
            weather_info['icon'] = icon_url.format(forecast_info.getAttribute('code'))

        return weather_info

    def getWeatherInfo(self, location, units='metric', lang='en'):
        """location must be a Yahoo weather location code
           unfortunately lang is not configurable for Yahoo weather
        """

        if units == 'metric':
            units = 'c'
        else:
            units = 'f'

        weather_info = self._getWeatherInfo(location, units)

        if 'error' in weather_info:
            warning = 'Yahoo! weather api returned this {0} error: {1}'
            logger.warning(warning.format(weather_info['error'],
                                          weather_info['text']))
        elif weather_info == {}:
            warning = 'Yahoo! weather api returned no information for location {0}'
            logger.warning(warning.format(location))

        return weather_info
