# -*- coding: utf-8 -*-

from collective.weather.interfaces import IWeatherSettings
from collective.weather.interfaces import IWeatherUtility
from collective.weather.testing import INTEGRATION_TESTING
from copy import deepcopy
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest


class UtilityTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.controlpanel = self.portal['portal_controlpanel']
        self.weather_utility = getUtility(IWeatherUtility)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_update_locations(self):
        self.weather_utility.update_locations()
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)
        old_ids = deepcopy(settings.location_ids)

        expected_values = [{'location_id': u'ARCA0023',
                            'name': u'Cordoba, Argentina',
                            'type': 'testprovider'},
                           {'location_id': u'USCA0638',
                            'name': u'Los Angeles, California',
                            'type': 'testprovider'}]

        actual_values = self.weather_utility.get_cities_list()

        self.assertEqual(actual_values, expected_values)

        # We add a new city to the registry
        settings.location_ids.append(u'LALA1212|New city, Test')

        expected_values = [{'location_id': u'ARCA0023',
                            'name': u'Cordoba, Argentina',
                            'type': 'testprovider'},
                           {'location_id': u'USCA0638',
                            'name': u'Los Angeles, California',
                            'type': 'testprovider'},
                           {'location_id': u'LALA1212',
                            'name': u'New city, Test',
                            'type': 'testprovider'}]

        actual_values = self.weather_utility.get_cities_list()

        self.assertEqual(actual_values, expected_values)

        # Finally, we add a malformed value to the list
        settings.location_ids.append('My city')

        expected_values = [{'location_id': u'ARCA0023',
                            'name': u'Cordoba, Argentina',
                            'type': 'testprovider'},
                           {'location_id': u'USCA0638',
                            'name': u'Los Angeles, California',
                            'type': 'testprovider'},
                           {'location_id': u'LALA1212',
                            'name': u'New city, Test',
                            'type': 'testprovider'}]

        actual_values = self.weather_utility.get_cities_list()

        self.assertEqual(actual_values, expected_values)

        # restore old values
        settings.location_ids = old_ids

    def test_update_weather_info(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)

        # Update weather info
        self.weather_utility.update_weather_info()

        expected_values = {u'USCA0638': {'conditions': u'Snowing',
                                         'temp': u'-8\xb0C',
                                         'icon': u'icon.png'},
                           u'ARCA0023': {'conditions': u'Windy',
                                         'temp': u'20\xb0C',
                                         'icon': u'icon.png'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        # Now, we add a new city
        old_locations = deepcopy(settings.location_ids)
        settings.location_ids.append(u'NEW123|New weather')

        self.weather_utility.update_weather_info()

        expected_values = {u'USCA0638': {'conditions': u'Snowing',
                                         'temp': u'-8\xb0C',
                                         'icon': u'icon.png'},
                           u'ARCA0023': {'conditions': u'Windy',
                                         'temp': u'20\xb0C',
                                         'icon': u'icon.png'},
                           u'NEW123': {'conditions': u'Snowing',
                                       'icon': u'icon.png',
                                       'temp': u'-8\xb0C'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        # If we remove the new city, then we should no longer get it
        settings.location_ids = old_locations

        self.weather_utility.update_weather_info()

        expected_values = {u'USCA0638': {'conditions': u'Snowing',
                                         'temp': u'-8\xb0C',
                                         'icon': u'icon.png'},
                           u'ARCA0023': {'conditions': u'Windy',
                                         'temp': u'20\xb0C',
                                         'icon': u'icon.png'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        # Test imperial units
        settings.units = 'imperial'
        self.weather_utility.weather_info = {}
        self.weather_utility.update_weather_info()

        expected_values = {u'USCA0638': {'conditions': u'Snowing',
                                         'temp': u'-8\xb0F',
                                         'icon': u'icon.png'},
                           u'ARCA0023': {'conditions': u'Windy',
                                         'temp': u'20\xb0F',
                                         'icon': u'icon.png'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

    def test_get_city(self):
        city = self.weather_utility.get_city('ARCA0023')
        expected_city = {'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'testprovider'}

        self.assertEqual(city, expected_city)

        city = self.weather_utility.get_city('ARCA00232')

        self.assertEqual(city, expected_city)

    def test_get_current_city(self):

        COOKIE_KEY = 'collective.weather.current_city'

        city = self.weather_utility.get_current_city()
        expected_city = {'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'testprovider'}

        self.assertEqual(city, expected_city)

        self.request.cookies[COOKIE_KEY] = 'USCA0638'

        city = self.weather_utility.get_current_city()
        expected_city = {'location_id': u'USCA0638',
                         'name': u'Los Angeles, California',
                         'type': 'testprovider'}

        self.assertEqual(city, expected_city)

        self.request.cookies[COOKIE_KEY] = 'USCA06385'

        city = self.weather_utility.get_current_city()
        expected_city = {'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'testprovider'}

        self.assertEqual(city, expected_city)

    def test_update_specific_weather_info(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)
        settings.units = 'metric'

        # What we first do is replace all locations created from the registry, with new values
        old_locations = deepcopy(settings.location_ids)
        settings.location_ids = [
            u'ARCA0024|Cordoba, Argentina',
            u'USCA0639|Los Angeles, California',
            u'NEW124|New weather',
            u'NEW125|New weather2',
        ]
        # And reset any existing weather info
        self.weather_utility.weather_info = {}

        # Update weather info for Los Angeles
        self.weather_utility.update_weather_info('USCA0639')

        expected_values = {u'USCA0639': {'conditions': u'Snowing',
                                         'temp': u'-10\xb0C',
                                         'icon': u'icon.png'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Now, for New weather2
        self.weather_utility.update_weather_info('NEW125')

        expected_values = {u'USCA0639': {'conditions': u'Snowing',
                                         'temp': u'-10\xb0C',
                                         'icon': u'icon.png'},
                           u'NEW125': {'conditions': u'Snowing',
                                       'icon': u'icon.png',
                                       'temp': u'-20\xb0C'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Now, if i ask for an invalid city, i should get for the first one
        self.weather_utility.update_weather_info('New weather3')

        expected_values = {u'ARCA0024': {'conditions': u'Windy',
                                         'temp': u'10\xb0C',
                                         'icon': u'icon.png'},
                           u'USCA0639': {'conditions': u'Snowing',
                                         'temp': u'-10\xb0C',
                                         'icon': u'icon.png'},
                           u'NEW125': {'conditions': u'Snowing',
                                       'icon': u'icon.png',
                                       'temp': u'-20\xb0C'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Finally, ask for New weather
        self.weather_utility.update_weather_info('NEW124')

        expected_values = {u'ARCA0024': {'conditions': u'Windy',
                                         'temp': u'10\xb0C',
                                         'icon': u'icon.png'},
                           u'USCA0639': {'conditions': u'Snowing',
                                         'temp': u'-10\xb0C',
                                         'icon': u'icon.png'},
                           u'NEW124': {'conditions': u'Snowing',
                                       'icon': u'icon.png',
                                       'temp': u'-20\xb0C'},
                           u'NEW125': {'conditions': u'Snowing',
                                       'icon': u'icon.png',
                                       'temp': u'-20\xb0C'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Restore original values
        settings.location_ids = old_locations
        # And reset any existing weather info
        self.weather_utility.weather_info = {}
