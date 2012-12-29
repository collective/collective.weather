# -*- coding: utf-8 -*-

import logging
import pywapi
import sys
import urllib2

from datetime import datetime

from zope.component import getUtility

from zope.globalrequest import getRequest

from zope.interface import implements

from plone.registry.interfaces import IRegistry

from collective.weather.interfaces import IWeatherUtility

from collective.weather.browser.interfaces import IYahooWeatherSchema

from collective.weather.config import COOKIE_KEY
from collective.weather.config import PROJECTNAME
from collective.weather.config import TIME_THRESHOLD

from collective.weather import _


logger = logging.getLogger(PROJECTNAME)


class WeatherUtility(object):
    implements(IWeatherUtility)

    weather_info = {}
    cities_list = []
    current_city = ''

    # def _update_google_locations(self):
    #     # XXX: We are not going to be using Google Weather, seems the API is
    #     # no longer supported.
    #     # http://blog.programmableweb.com/2012/08/28/google-weather-api-never-supported-finally-disconnected/
    #     registry = getUtility(IRegistry)
    #     settings = registry.forInterface(IGoogleWeatherSchema)
    #     if settings.google_location_ids:
    #         for i in settings.google_location_ids:
    #             try:
    #                 id,name,location_id = i.split('|')
    #             except ValueError:
    #                 continue

    #             result = {'id': id,
    #                       'name': name,
    #                       'location_id': location_id,
    #                       'type': 'google'}

    #             self.cities_list.append(result)

    def _update_yahoo_locations(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IYahooWeatherSchema)
        if settings.yahoo_location_ids:
            for i in settings.yahoo_location_ids:
                try:
                    id, name, location_id = i.split('|')
                except ValueError:
                    logger.warning("Malformed line: %s" % i)
                    continue

                result = {'id': id,
                          'name': name,
                          'location_id': location_id,
                          'type': 'yahoo'}

                self.cities_list.append(result)

    # def _update_google_weather_info(self, city_id=None):
    #     # XXX: We are not going to be using Google Weather, seems the API is
    #     # no longer supported.
    #     # http://blog.programmableweb.com/2012/08/28/google-weather-api-never-supported-finally-disconnected/
    #     registry = getUtility(IRegistry)
    #     settings = registry.forInterface(IGoogleWeatherSchema)
    #     units = settings.google_units
    #     lang = settings.google_language

    #     now = datetime.now()
    #     for city in self.cities_list:

    #         if city_id and city['id'] != city_id:
    #             continue

    #         if city['type'] != 'google':
    #             continue

    #         old_data = self.get_weather_info(city)

    #         if old_data and old_data.get('date'):
    #             if old_data.get('date') > now - TIME_THRESHOLD:
    #                 continue

    #         try:
    #             result = pywapi.get_weather_from_google(city['location_id'].encode('utf-8'), hl=lang)
    #         except urllib2.URLError:
    #             result = ""
    #         except:
    #             # Just avoid any error silently
    #             result = ""

    #         if result and 'current_conditions' in result:
    #             try:
    #                 conditions = result['current_conditions']

    #                 if units == 'imperial':
    #                     temp = _(u"%sºF") % conditions['temp_f']
    #                 else:
    #                     temp = _(u"%sºC") % conditions['temp_c']

    #                 new_weather = {'temp': temp,
    #                                'conditions': conditions['condition'],
    #                                'icon': u"http://www.google.com%s" % conditions.get('icon', '')}

    #                 self.weather_info[city['id']] = {'date': now,
    #                                                  'weather': new_weather}
    #             except:
    #                 if city['id'] in self.weather_info:
    #                     del self.weather_info[city['id']]
    #         else:
    #             if city['id'] in self.weather_info:
    #                 del self.weather_info[city['id']]

    def _update_yahoo_weather_info(self, city_id=None):
        start_update = datetime.now()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IYahooWeatherSchema)
        units = settings.yahoo_units

        now = start_update

        if city_id:
            logger.info("Update Yahoo Weather: %s" % city_id)
            cities_list = [city['id'] for city in self.cities_list]
            if city_id in cities_list:
                # If asked city exists in our list of cities, find it
                match = [i for i in self.cities_list if city_id == i['id']]
                to_update = [match[0]]
            else:
                logger.warning("Requested city '%s' is not a valid city, updating first one of the list" % city_id)
                # If asked city does not exist, update first one
                to_update = [self.cities_list[0]]
        else:
            # If no asked city, just update all of them
            logger.info("Update Yahoo Weather for all cities")
            to_update = self.cities_list

        for city in to_update:
            if city['type'] != 'yahoo':
                continue

            old_data = self.get_weather_info(city)

            if old_data and old_data.get('date'):
                if old_data.get('date') > now - TIME_THRESHOLD:
                    logger.info("Last update was done %s. Not updating again" % old_data.get('date'))
                    continue

            try:
                cityid = city['location_id'].encode('utf-8')
                logger.info("Getting data for city: %s" % cityid)
                result = pywapi.get_weather_from_yahoo(cityid, units=units)
                logger.info("Result: %s" % result)
            except urllib2.URLError as e:
                logger.warning("The server returned an error: %s" % e)
                result = ""
            except:
                logger.warning("There was an error when contacting the remote server: %s" % sys.exc_info()[0])
                # Just avoid any error silently
                result = ""

            if result and 'condition' in result:
                try:
                    conditions = result['condition']

                    if units == 'imperial':
                        temp = _(u"%sºF") % conditions['temp']
                    else:
                        temp = _(u"%sºC") % conditions['temp']

                    new_weather = {'temp': temp,
                                   'conditions': conditions['text'],
                                   'icon': u"http://l.yimg.com/a/i/us/we/52/%s.gif" % conditions.get('code', '')}

                    self.weather_info[city['id']] = {'date': now,
                                                     'weather': new_weather}
                except:
                    if city['id'] in self.weather_info:
                        logger.warning("Something went wrong, removing weather data for city: %s" % city['id'])
                        del self.weather_info[city['id']]
            else:
                if city['id'] in self.weather_info:
                    logger.warning("No 'condition' in result, removing weather data for city: %s" % city['id'])
                    del self.weather_info[city['id']]

        for city in self.weather_info.keys():
            match = [i for i in self.cities_list if city == i['id']]
            if not match:
                logger.warning("The city %s is not listed in the list of cities. Removing weather data" % city)
                del self.weather_info[city]

        end_update = datetime.now()
        took = end_update - start_update
        logger.info("Yahoo! update took: %s" % took)

    def update_locations(self):
        self.cities_list = []
        #self._update_google_locations()
        self._update_yahoo_locations()

    def get_cities_list(self):
        self.update_locations()
        return self.cities_list

    def update_weather_info(self, city=None):
        self.update_locations()
        #self._update_google_weather_info(city)
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
            logger.warning("Requested city '%s' is not a valid city, returning the first one of the list: %s" % (city, result['id']))

        return result

    def get_current_city(self):
        # We should get it from a cookie in case of anonymous, and somewhere else
        # from authenticated
        self.update_locations()
        result = ''
        request = getRequest()
        if len(self.cities_list) > 0:
            cookie = COOKIE_KEY % "current_city"
            value = request.cookies.get(cookie, '')
            if not value:
                result = self.cities_list[0]
                logger.info("No cookie was present, returning first available city: %s" % result)
            else:
                logger.info("Cookie present, getting city: %s" % value)
                result = self.get_city(value)

        return result
