# -*- coding: utf-8 -*-

###################################################################
#
# Weather Underground API documentation
# http://www.wunderground.com/weather/api/d/docs?d=data/index&MR=1
#
# Create a free account
# http://www.wunderground.com/weather/api/d/login.html
#
# Create your api key
# http://www.wunderground.com/weather/api/d/questionnaire.html?
# plan=a&level=0&history=0
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

    >>> wunderground = utility('')
    >>> wunderground.getWeatherInfo('25,20')
    collective.weather - WARNING - Missing Weather Underground api key

    Initialize the utility with the provider's key

    >>> key = 'my-secret-key'
    >>> wunderground = utility(key)
    >>> wunderground.key
    'my-secret-key'

    Monkey patch _getWeatherInfo to avoid actual web service call

    >>> def _getWeatherInfo(location, units, lang):
    ...    weather_infos = {
    ...        'Argentina/Buenos_Aires,C,SP': {'temperature': 18.84,
    ...                                        'summary': 'Soleado',
    ...                                        'icon': 'sunny-icon.png'},
    ...        'Argentina/Buenos_Aires,F,EN': {'temperature': 65.91,
    ...                                        'summary': 'Sunny',
    ...                                        'icon': 'sunny-icon.png'}
    ...    }
    ...    key = '{0},{1},{2}'.format(location, units, lang)
    ...    if key in weather_infos:
    ...        return weather_infos[key]
    ...    else:
    ...        return {}

    >>> wunderground._getWeatherInfo = _getWeatherInfo

    Test with a known location and special lang code

    >>> info = wunderground.getWeatherInfo('Argentina/Buenos Aires', \
                                           units='C', lang='es')
    >>> '%.2f' % info['temperature']  # For Python 2.6
    '18.84'
    >>> info['summary']
    'Soleado'
    >>> info['icon']
    'sunny-icon.png'

    Test with a known location without unit and unknown lang code

    >>> info = wunderground.getWeatherInfo('Argentina/Buenos Aires', \
                                           lang='XX')
    >>> '%.2f' % info['temperature']  # For Python 2.6
    '65.91'
    >>> info['summary']
    'Sunny'

    Test a non existing (not registered) location

    >>> info = wunderground.getWeatherInfo('Hogwarts/The Kitchen', \
                                           units='C')
    >>> info
    {}
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

    def _getWeatherInfo(self, location, units='F', lang=None):
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

    def getWeatherInfo(self, location, units='F', lang=None):
        """location can be a:
           - tuplish (lat, lang)
           - US state/city
           - US zip/city
           - Country (or its wunderground non-iso code)/city
        """

        if self.key.strip() == '':
            logger.warning(u'Missing Weather Underground api key')
            return None

        # location might be a tuplish lat, lang
        if isinstance(location, (list, tuple)):
            location = ','.join(location)

        location = location.replace(' ', '_')

        lang = self._convert_special_langs(lang)

        weather_info = self._getWeatherInfo(location, units, lang)

        if 'error' in weather_info:
            warning = 'Weather Underground api returned this {0} error: {1}'
            logger.warning(warning.format(weather_info['error'],
                                          weather_info['text']))

        return weather_info
