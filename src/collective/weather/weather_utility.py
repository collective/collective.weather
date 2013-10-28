# -*- coding: utf-8 -*-

from collective.weather import _
from collective.weather.interfaces import IWeatherSettings
from collective.weather.config import COOKIE_KEY
from collective.weather.config import PROJECTNAME
from collective.weather.config import TIME_THRESHOLD
from collective.weather.interfaces import IWeatherUtility
from datetime import datetime
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implements

import logging
import pywapi
import sys
import urllib2


logger = logging.getLogger(PROJECTNAME)


class WeatherUtility(object):
    implements(IWeatherUtility)

    weather_info = {}
    cities_list = []
    current_city = ''

    def _update_yahoo_locations(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)
        if settings.location_ids:
            for i in settings.location_ids:
                try:
                    id, name, location_id = i.split('|')
                except ValueError:
                    logger.warning(u'Malformed line: %s' % i)
                    continue

                result = {'id': id,
                          'name': name,
                          'location_id': location_id,
                          'type': 'yahoo'}

                self.cities_list.append(result)

    def _update_yahoo_weather_info(self, city_id=None):
        start_update = datetime.now()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)
        units = settings.units

        now = start_update

        if city_id:
            logger.info(u'Update Yahoo Weather: {0}'.format(city_id))
            cities_list = [city['id'] for city in self.cities_list]
            if city_id in cities_list:
                # If asked city exists in our list of cities, find it
                match = [i for i in self.cities_list if city_id == i['id']]
                to_update = [match[0]]
            else:
                logger.warning(
                    u'Requested city "{0}" is not a valid city, '
                    u'updating first one of the list'.format(city_id))
                # If asked city does not exist, update first one
                to_update = [self.cities_list[0]]
        else:
            # If no asked city, just update all of them
            logger.info(u'Update Yahoo Weather for all cities')
            to_update = self.cities_list

        for city in to_update:
            if city['type'] != 'yahoo':
                continue

            old_data = self.get_weather_info(city)

            if old_data and old_data.get('date'):
                if old_data.get('date') > now - TIME_THRESHOLD:
                    logger.info(u'Last update was done %s. Not updating again' % old_data.get('date'))
                    continue

            try:
                cityid = city['location_id'].encode('utf-8')
                logger.info(u'Getting data for city: ' + cityid)
                result = pywapi.get_weather_from_yahoo(cityid, units=units)
                logger.info(u'Result: {0}'.format(result))
            except urllib2.URLError as e:
                logger.warning(u'The server returned an error: %s' % e)
                result = ''
            except:
                logger.warning(
                    u'There was an error when contacting the remote '
                    u'server: {0}'.format(sys.exc_info()[0]))
                # Just avoid any error silently
                result = ''

            if result and 'condition' in result and\
                ('temp' in result['condition'] and
                 'text' in result['condition'] and
                 'code' in result['condition']):

                conditions = result['condition']

                if units == 'imperial':
                    temp = _(u'%sºF') % conditions['temp']
                else:
                    temp = _(u'%sºC') % conditions['temp']

                new_weather = {'temp': temp,
                               'conditions': conditions['text'],
                               'icon': u'http://l.yimg.com/a/i/us/we/52/%s.gif' % conditions.get('code', '')}

                self.weather_info[city['id']] = {'date': now,
                                                 'weather': new_weather}
            else:
                logger.warning(u'No "condition" in result, or malformed response.')

        for city in self.weather_info.keys():
            match = [i for i in self.cities_list if city == i['id']]
            if not match:
                logger.warning('The city %s is not listed in the list of cities. Removing weather data' % city)
                del self.weather_info[city]

        end_update = datetime.now()
        took = end_update - start_update
        logger.info('Yahoo! update took: %s' % took)

    def update_locations(self):
        self.cities_list = []
        self._update_yahoo_locations()

    def get_cities_list(self):
        self.update_locations()
        return self.cities_list

    def update_weather_info(self, city=None):
        self.update_locations()
        self._update_yahoo_weather_info(city)

    def get_weather_info(self, city=None):
        if not city:
            result = self.weather_info
        else:
            result = self.weather_info.get(city['id'], None)

        return result

    def get_city(self, city):
        self.update_locations()
        match = [i for i in self.cities_list if i['id'] == city]
        if match:
            result = match[0]
        else:
            result = self.cities_list[0]
            logger.warning(
                u'Requested city "{0}" is not a valid city, returning the '
                u'first one of the list: {1}'.format(city, result['id']))

        return result

    def get_current_city(self):
        # We should get it from a cookie in case of anonymous, and somewhere else
        # from authenticated
        self.update_locations()
        result = ''
        request = getRequest()
        if len(self.cities_list) > 0:
            cookie = COOKIE_KEY % 'current_city'
            value = request.cookies.get(cookie, '')
            if not value:
                result = self.cities_list[0]
                logger.info(u'No cookie was present, returning first available city: %s' % result)
            else:
                logger.info(u'Cookie present, getting city: %s' % value)
                result = self.get_city(value)

        return result
