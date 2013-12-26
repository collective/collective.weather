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

        WEATHER = {
            'ARCA0023': {'summary': u'Windy',
                         'temperature': 20,
                         'icon': u'icon.png'},

            'USCA0638': {'summary': u'Snowing',
                         'temperature': -8,
                         'icon': u'icon.png'},

            'NEW123': {'summary': u'Snowing',
                       'temperature': -8,
                       'icon': u'icon.png'},

            'NEW123-invalid': {'temperature': -8,
                               'icon': u'icon.png'},

            'ARCA0024': {'summary': u'Windy',
                         'temperature': 10,
                         'icon': u'icon.png'},

            'USCA0639': {'summary': u'Snowing',
                         'temperature': -10,
                         'icon': u'icon.png'},

            'NEW124': {'summary': u'Snowing',
                       'temperature': -20,
                       'icon': u'icon.png'},

            'NEW125': {'summary': u'Snowing',
                       'temperature': -20,
                       'icon': u'icon.png'}
        }

        if location == 'ARBA0023-urllib-exception':
            raise urllib2.URLError('')
        elif location == 'ARBA0023-exception':
            raise ValueError
        else:
            weather_info = WEATHER[location]

        if 'error' in weather_info:
            warning = 'Test weather api returned this {0} error: {1}'
            logger.warning(warning.format(weather_info['error'],
                                          weather_info['text']))
        elif weather_info == {}:
            warning = 'Test weather api returned no information for location {0}'
            logger.warning(warning.format(location))

        return weather_info
