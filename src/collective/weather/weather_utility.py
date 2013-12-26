# -*- coding: utf-8 -*-

from collective.weather.interfaces import IWeatherSettings
from collective.weather.config import COOKIE_KEY
from collective.weather.config import PROJECTNAME
from collective.weather.config import TIME_THRESHOLD
from collective.weather.interfaces import IWeatherInfo
from collective.weather.interfaces import IWeatherUtility
from datetime import datetime
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope.interface import implements

import logging

logger = logging.getLogger(PROJECTNAME)


class WeatherUtility(object):
    implements(IWeatherUtility)

    weather_info = {}
    cities_list = []
    current_city = ''

    def _update_weather_info(self, city_id=None):
        start_update = datetime.now()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)
        units = settings.units
        degrees = 'C'
        if units == 'imperial':
            degrees = 'F'

        provider = settings.weather_api
        api_key = settings.weather_api_key

        now = start_update

        if city_id:
            logger.info(u'Update Weather: {0}'.format(city_id))
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
            logger.info(u'Update Weather for all cities')
            to_update = self.cities_list

        for city in to_update:

            old_data = self.get_weather_info(city)

            if old_data and old_data.get('date'):
                if old_data.get('date') > now - TIME_THRESHOLD:
                    logger.info(u'Last update was done %s. Not updating again' % old_data.get('date'))
                    continue

            cityid = city['location_id'].encode('utf-8')
            logger.info(u'Getting data for city: ' + cityid)
            utility = queryUtility(IWeatherInfo, name=provider)
            if utility:
                weather_api = utility(api_key)
                portal = getSite()
                ltool = getToolByName(portal, 'portal_languages')
                try:
                    result = weather_api.getWeatherInfo(cityid, units=units, lang=ltool.getDefaultLanguage())
                except Exception, msg:
                    result = {'error': msg}
            logger.info(u'Result: {0}'.format(result))

            if not result == {} and not 'error' in result and \
               'temperature' in result and \
               'summary' in result and \
               'icon' in result:
                temp = result.get('temperature', None)
                if temp:
                    temp = u'{0}\xb0{1}'.format(temp, degrees)

                new_weather = {'temp': temp,
                               'conditions': result.get('summary', None),
                               'icon': result.get('icon', None)}

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
        logger.info('Weather update took: %s' % took)

    def update_locations(self):
        self.cities_list = []
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
                          'type': settings.weather_api}

                self.cities_list.append(result)

    def get_cities_list(self):
        self.update_locations()
        return self.cities_list

    def update_weather_info(self, city=None):
        self.update_locations()
        self._update_weather_info(city)

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
