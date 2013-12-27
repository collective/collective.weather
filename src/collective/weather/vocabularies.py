# -*- coding: utf-8 -*-

from collective.weather.interfaces import IWeatherInfo
from collective.weather.interfaces import IWeatherUtility
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary


def LocationsVocabulary(context):
    """Creates a vocabulary to expose configured locations.
    """

    weather_utility = getUtility(IWeatherUtility)
    locations = weather_utility.get_cities_list()
    items = []
    for l in locations:
        items.append(
            SimpleVocabulary.createTerm(l['location_id'], l['location_id'], l['name']))

    return SimpleVocabulary(items)


def WeatherInfoProviders(context):
    """Creates a vocabulary of all the named utilities
       that implement IWeatherInfo interface.
    """
    utilities = getUtilitiesFor(IWeatherInfo)
    items = []
    for utility in utilities:
        items.append(SimpleVocabulary.createTerm(utility[0]))

    return SimpleVocabulary(items)
