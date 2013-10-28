# -*- coding: utf-8 -*-

from collective.weather.interfaces import IWeatherUtility
from collective.weather.interfaces import IWeatherSettings
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility


class TopBarWeatherViewlet(ViewletBase):

    index = ViewPageTemplateFile('top_bar_weather.pt')
    cities_list = []
    current_city = ''

    def __init__(self, *args, **kw):
        super(TopBarWeatherViewlet, self).__init__(*args, **kw)
        self.weather_utility = getUtility(IWeatherUtility)

    def available(self):
        """Show weather viewlet on site top?
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)
        return getattr(settings, 'show_viewlet', False)

    def update(self):
        super(TopBarWeatherViewlet, self).update()

        self.cities_list = self.weather_utility.get_cities_list()
        self.weather_info = self.weather_utility.get_weather_info()
