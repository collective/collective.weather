# -*- coding: utf-8 -*-

""" Test named utility for IWeatherInfo
"""

from collective.weather.config import PROJECTNAME
from collective.weather.interfaces import IWeatherInfo
from zope.interface import implements

import logging
import urllib2

logger = logging.getLogger(PROJECTNAME)


class TestProvider(object):
    """Test weather implementation of IWeatherInfo
    """

    implements(IWeatherInfo)

    def __init__(self, key=None):
        self.key = key

    def getWeatherInfo(self, location, units='metric', lang='en'):
        """Dummy implementation of getWeatherInfo for testing puroposes
        """

        if location == 'ARCA0023':
            weather_info = {'summary': u'Windy',
                            'temperature': 20,
                            'icon': u'icon.png'}

        if location == 'USCA0638':
            weather_info = {'summary': u'Snowing',
                            'temperature': -8,
                            'icon': u'icon.png'}

        if location == 'NEW123':
            weather_info = {'summary': u'Snowing',
                            'temperature': -8,
                            'icon': u'icon.png'}

        if location == 'NEW123-invalid':
            weather_info = {'temperature': -8,
                            'icon': u'icon.png'}

        if location == 'ARBA0023-urllib-exception':
            raise urllib2.URLError('')

        if location == 'ARBA0023-exception':
            raise ValueError

        if location == 'ARCA0024':
            weather_info = {'summary': u'Windy',
                            'temperature': 10,
                            'icon': u'icon.png'}

        if location == 'USCA0639':
            weather_info = {'summary': u'Snowing',
                            'temperature': -10,
                            'icon': u'icon.png'}

        if location == 'NEW124':
            weather_info = {'summary': u'Snowing',
                            'temperature': -20,
                            'icon': u'icon.png'}

        if location == 'NEW125':
            weather_info = {'summary': u'Snowing',
                            'temperature': -20,
                            'icon': u'icon.png'}

        if 'error' in weather_info:
            warning = 'Test weather api returned this {0} error: {1}'
            logger.warning(warning.format(weather_info['error'],
                                          weather_info['text']))
        elif weather_info == {}:
            warning = 'Test weather api returned no information for location {0}'
            logger.warning(warning.format(location))

        return weather_info
