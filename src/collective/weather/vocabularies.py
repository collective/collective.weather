# -*- coding: utf-8 -*-

from collective.weather.interfaces import IWeatherUtility
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary


def CitiesVocabulary(context):
    """ Creates a vocabulary to expose configured cities.
    """

    weather_utility = getUtility(IWeatherUtility)
    cities_list = weather_utility.get_cities_list()
    items = []
    for city in cities_list:
        items.append(SimpleVocabulary.createTerm(
                     city['id'], city['location_id'], city['name']))

    return SimpleVocabulary(items)
