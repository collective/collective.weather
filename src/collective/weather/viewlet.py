# -*- coding: utf-8 -*-

import pywapi
import urllib2

from datetime import datetime
from datetime import timedelta

from Acquisition import aq_inner

from zope.annotation import IAnnotations
from zope.component import getUtility

from plone.app.layout.viewlets.common import ViewletBase

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.weather.browser.interfaces import IGoogleWeatherSchema
# from collective.weather.browser.interfaces import IYahooWeatherSchema
# from collective.weather.browser.interfaces import INoaaWeatherSchema

from collective.weather.config import COOKIE_KEY
from collective.weather import _

# Time that should pass before fetching new weather information.
TIME_THRESHOLD = timedelta(minutes=30)


class TopBarWeatherViewlet(ViewletBase):

    index = ViewPageTemplateFile('top_bar_weather.pt')
    weather_info= {}
    cities_list = []
    current_city = ''

    def update_google_locations(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGoogleWeatherSchema)
        for i in settings.google_location_ids:
            try:
                id,name,location_id = i.split('|')
            except ValueError:
                continue

            result = {'id': id,
                      'name': name,
                      'location_id': location_id,
                      'type': 'google'}

            self.cities_list.append(result)

    def update_google_weather_info(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGoogleWeatherSchema)
        units = settings.google_units
        lang = settings.google_language

        now = datetime.now()
        for city in self.cities_list:
            if city['type'] != 'google':
                continue

            old_data = self.weather_info.get(city['id'], None)

            if old_data and old_data.get('date'):
                if old_data.get('date') > now - TIME_THRESHOLD:
                    continue

            try:
                result = pywapi.get_weather_from_google(city['location_id'].encode('utf-8'), hl=lang)
            except urllib2.URLError:
                result = ""

            if result:
                if units == 'imperial':
                    temp = _(u"%sºF") % result['current_conditions']['temp_f']
                else:
                    temp = _(u"%sºC") % result['current_conditions']['temp_c']

                new_weather = {'temp': temp,
                               'conditions': result['current_conditions']['condition'],
                               'icon': u"http://www.google.com%s" % result['current_conditions']['icon']}

                self.weather_info[city['id']] = {'date': now,
                                                 'weather': new_weather}

            else:
                self.weather_info[city['id']] = {'weather': ""}

    def get_current_city(self):
        # We should get it from a cookie in case of anonymous, and somewhere else
        # from authenticated
        result = ''
        if len(self.cities_list) > 0:
            cookie = COOKIE_KEY % "top_weather"
            value = self.request.cookies.get(cookie, '')
            if not value:
                result = self.cities_list[0]
            else:
                match = [i for i in self.cities_list if i['id'] == value]
                if match:
                    result = match[0]
                else:
                    result = self.cities_list[0]


        return result

    def set_current_city(self):
        city = self.request.get('city_weather', None)
        if city:
            # We should store the current city in a cookie
            cookie = COOKIE_KEY % "top_weather"
            expires = 'Wed, 19 Feb 2020 14:28:00 GMT'
            city = str(city)
            self.request.response[cookie] = city
            self.request.response.setCookie(cookie,
                                            city,
                                            path='/',
                                            expires=expires)
            
            self.request.response.redirect(self.context.absolute_url())


    def update(self):
        super(TopBarWeatherViewlet, self).update()
        self.set_current_city()

        self.cities_list = []
        self.current_city = ''

        # For now, we only support Google weather information
        self.update_google_locations()
        self.update_google_weather_info()

        self.current_city = self.get_current_city()

