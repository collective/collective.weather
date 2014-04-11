# -*- coding: utf-8 -*-

""" Weather Underground API documentation
    http://www.wunderground.com/weather/api/d/docs?d=data/index&MR=1

    Create a free account
    http://www.wunderground.com/weather/api/d/login.html

    Create your api key
    http://www.wunderground.com/weather/api/d/questionnaire.html?
    plan=a&level=0&history=0
"""


from collective.weather.config import PROJECTNAME
from collective.weather.interfaces import IWeatherInfo
from urllib2 import HTTPError
from urllib2 import urlopen
from zope.interface import implements

import json
import logging

logger = logging.getLogger(PROJECTNAME)

LANG_CODES = {
    'be': 'BY',
    'bg': 'BU',
    'cs': 'CZ',
    'da': 'DK',
    'de': 'DL',
    'el': 'GR',
    'en': 'LI',
    'es': 'SP',
    'ga': 'IR',
    'gl': 'GZ',
    'he': 'IL',
    'hr': 'CR',
    'ja': 'JP',
    'jv': 'JW',
    'ko': 'KR',
    'pt': 'BR',
    'sq': 'AL',
    'sv': 'SW',
    'sw': 'SI',
    'uk': 'UA',
    'vi': 'VU',
    'wo': 'SN',
    'zh': 'CN',
    'zh': 'TW'
}


class Wunderground(object):
    """ Weather underground implementation of IWeatherInfo
    """

    implements(IWeatherInfo)

    BASE_URL = 'http://api.wunderground.com/api/{0}/conditions/' \
               'lang:{1}/q/{2}.json'

    def __init__(self, key=None):
        self.key = key

    def _convert_special_langs(self, lang):
        if not lang:
            return 'EN'  # Default language for Weather Underground
        elif lang.lower() in LANG_CODES:
            return LANG_CODES[lang.lower()]
        else:  # Try with the upper version of the lang code
            return lang.upper()

    def _getWeatherInfo(self, location, units='C', lang=None):
        """Helper method to call the remote web service and
           to return a simple dictionary
        """

        url = self.BASE_URL
        try:
            response = urlopen(url.format(self.key, lang, location))
        except HTTPError, error:
            return {'error': error.code, 'text': error.reason}

        forecast_info = json.loads(response.read())
        if 'current_observation' in forecast_info:
            forecast_info = forecast_info['current_observation']
        else:
            forecast_info = {}

        temp_response = 'temp_{0}'.format(units.lower())

        weather_info = {}
        if temp_response in forecast_info and \
           'weather' in forecast_info and \
           'icon_url' in forecast_info:
            weather_info = {}
            weather_info['temperature'] = forecast_info[temp_response]
            weather_info['summary'] = forecast_info['weather']
            weather_info['icon'] = forecast_info['icon_url']

        return weather_info

    def getWeatherInfo(self, location, units='metric', lang='en'):
        """location can be a:
           - tuplish (lat, lang)
           - US state/city
           - US zip/city
           - Country (or its wunderground non-iso code)/city
        """

        if not self.key:
            msg = u'Missing Weather Underground API key'
            logger.warning(msg)
            raise ValueError(msg)

        # location might be a tuplish lat, lang
        if isinstance(location, (list, tuple)):
            location = ','.join(location)

        location = location.replace(' ', '_')

        if units == 'metric':
            units = 'C'
        else:
            units = 'F'

        lang = self._convert_special_langs(lang)

        weather_info = self._getWeatherInfo(location, units, lang)

        if 'error' in weather_info:
            warning = 'Weather Underground api returned this {0} error: {1}'
            logger.warning(warning.format(weather_info['error'],
                                          weather_info['text']))
        elif weather_info == {}:
            warning = 'Weather Underground api returned no information for location {0}'
            logger.warning(warning.format(location))

        return weather_info
