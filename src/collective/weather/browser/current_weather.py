# -*- coding: utf-8 -*-

from zope.component import getUtility

from Products.Five.browser import BrowserView

from collective.weather.interfaces import IWeatherUtility


class CurrentWeather(BrowserView):

    def __call__(self):
        weather_utility = getUtility(IWeatherUtility)
        if 'city' in self.request:
            city = self.request.get('city')
            weather_utility.set_current_city(city)
            self.current_city = weather_utility.get_city(city)
        else:
            self.current_city = weather_utility.get_current_city()
        
        if self.current_city:
            self.weather_info = weather_utility.get_weather_info(self.current_city)
        else:
            self.weather_info = None

        return super(CurrentWeather, self).__call__()

class UpdateWeather(BrowserView):

    def __call__(self):
        weather_utility = getUtility(IWeatherUtility)

        city = None
        if 'city' in self.request:
            city = self.request.get('city')
        
        weather_utility.update_weather_info(city)
        
        return True

