# -*- coding: utf-8 -*-

import logging

from zope.component import getUtility
from zope.component import queryUtility

from Products.Five.browser import BrowserView

from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.cachepurging.interfaces import IPurger

from plone.cachepurging.utils import getURLsToPurge
from plone.cachepurging.utils import isCachePurgingEnabled

from plone.registry.interfaces import IRegistry

from collective.weather.config import PROJECTNAME
from collective.weather.interfaces import IWeatherUtility


logger = logging.getLogger(PROJECTNAME)


class CurrentWeather(BrowserView):

    def __call__(self):
        weather_utility = getUtility(IWeatherUtility)
        if 'city' in self.request:
            city = self.request.get('city')
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
        success = True
        weather_utility = getUtility(IWeatherUtility)

        city = None
        if 'city' in self.request:
            city = self.request.get('city')

        updated = weather_utility.update_weather_info(city)

        if not updated:
            success = False

            purger = queryUtility(IPurger)

            logger.info("Weather update for city '%s' failed." % city)
            if isCachePurgingEnabled() and purger and city:
                # If we are using a cache, we are going to want to not have the update-weather and current-weather
                # cached for this city. Notifying to be purged here.
                # XXX: We cannot just purge "self.context" because each city has its own
                # url/@@update-weather?city=city_name so we forge the URL here
                # and purge it manually. Basically, the same that plone.cachepurging
                # does in hooks.purge

                logger.info("Trying to purge the cache")
                registry = queryUtility(IRegistry)
                settings = registry.forInterface(ICachePurgingSettings, check=False)

                context_path = self.context.absolute_url_path()
                views = ["update-weather", "current-weather"]

                for view in views:
                    for url in getURLsToPurge("%s/@@%s?city=%s" %
                                              (context_path, view, city),
                                              settings.cachingProxies):
                        logger.info("Purge url: %s" % url)
                        purger.purgeAsync(url)

        return success
