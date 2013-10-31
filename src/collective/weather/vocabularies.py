# -*- coding: utf-8 -*-

from collective.weather.interfaces import IWeatherUtility
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
            SimpleVocabulary.createTerm(l['id'], l['location_id'], l['name']))

    return SimpleVocabulary(items)
