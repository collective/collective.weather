# -*- coding: utf-8 -*-

from zope.component import getUtility

from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.weather.interfaces import IWeatherUtility


class TopBarWeatherViewlet(ViewletBase):

    index = ViewPageTemplateFile('top_bar_weather.pt')
    cities_list = []
    current_city = ''

    def __init__(self, *args, **kw):
        super(TopBarWeatherViewlet, self).__init__(*args, **kw)
        self.weather_utility = getUtility(IWeatherUtility)

    def update(self):
        super(TopBarWeatherViewlet, self).update()
        
        self.cities_list = self.weather_utility.get_cities_list()
        self.weather_info = self.weather_utility.get_weather_info()
