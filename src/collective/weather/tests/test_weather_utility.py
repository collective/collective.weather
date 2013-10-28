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

        expected_values = [{'id': u'Cordoba',
                            'location_id': u'ARCA0023',
                            'name': u'Cordoba, Argentina',
                            'type': 'yahoo'},
                           {'id': u'Los Angeles',
                            'location_id': u'USCA0638',
                            'name': u'Los Angeles, California',
                            'type': 'yahoo'}]

        actual_values = self.weather_utility.get_cities_list()

        self.assertEqual(actual_values, expected_values)

        # We add a new city to the registry
        settings.location_ids.append(u'New city|New city, Test|LALA1212')

        expected_values = [{'id': u'Cordoba',
                            'location_id': u'ARCA0023',
                            'name': u'Cordoba, Argentina',
                            'type': 'yahoo'},
                           {'id': u'Los Angeles',
                            'location_id': u'USCA0638',
                            'name': u'Los Angeles, California',
                            'type': 'yahoo'},
                           {'id': u'New city',
                            'location_id': u'LALA1212',
                            'name': u'New city, Test',
                            'type': 'yahoo'}]

        actual_values = self.weather_utility.get_cities_list()

        self.assertEqual(actual_values, expected_values)

        # Finally, we add a malformed value to the list
        settings.location_ids.append('My city')

        expected_values = [{'id': u'Cordoba',
                            'location_id': u'ARCA0023',
                            'name': u'Cordoba, Argentina',
                            'type': 'yahoo'},
                           {'id': u'Los Angeles',
                            'location_id': u'USCA0638',
                            'name': u'Los Angeles, California',
                            'type': 'yahoo'},
                           {'id': u'New city',
                            'location_id': u'LALA1212',
                            'name': u'New city, Test',
                            'type': 'yahoo'}]

        actual_values = self.weather_utility.get_cities_list()

        self.assertEqual(actual_values, expected_values)

        #restore old values
        settings.location_ids = old_ids

    def test_update_weather_info(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)

        # Update weather info
        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'20\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        # Now, we add a new city
        old_locations = deepcopy(settings.location_ids)
        settings.location_ids.append(u'New weather|New weather|NEW123')

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'20\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'New weather': {'conditions': u'Snowing',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif',
                                            'temp': u'-8\xbaC'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        # If we remove the new city, then we should no longer get it
        settings.location_ids = old_locations

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'20\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        # We are going to forge weather info into the utility so we simulate invalid returned values and errors
        self.weather_utility.weather_info['New weather'] = {'weather': {'conditions': u'Snowing',
                                                                        'temp': u'-8\xbaC',
                                                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        # We create a city with the same name but different location_id, so we can simulate
        # invalid results for an existing city. In this case, we should still see old data
        settings.location_ids.append(u'New weather|New weather|NEW123-invalid')
        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'20\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'New weather': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        self.weather_utility.weather_info['Buenos Aires'] = {'weather': {'conditions': u'Snowing',
                                                                         'temp': u'-8\xbaC',
                                                                         'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        # If we get a urllib exception, then also keep the existing value
        settings.location_ids.append(u'Buenos Aires|Buenos Aires, Argentina|ARBA0023-urllib-exception')

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'20\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'New weather': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Buenos Aires': {'conditions': u'Snowing',
                                             'temp': u'-8\xbaC',
                                             'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])
        self.assertEqual(actual_values, expected_values)

        # If we get a any exception, then also keep the existing value
        settings.location_ids.append(u'Buenos Aires|Buenos Aires, Argentina|ARBA0023-exception')

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'20\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'New weather': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Buenos Aires': {'conditions': u'Snowing',
                                             'temp': u'-8\xbaC',
                                             'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

        # Test imperial units
        settings.units = 'imperial'
        self.weather_utility.weather_info = {}
        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-8\xbaF',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'20\xbaF',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEqual(actual_values, expected_values)

    def test_get_city(self):
        city = self.weather_utility.get_city('Cordoba')
        expected_city = {'id': u'Cordoba',
                         'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'yahoo'}

        self.assertEqual(city, expected_city)

        city = self.weather_utility.get_city('Cordoba2')

        self.assertEqual(city, expected_city)

    def test_get_current_city(self):

        COOKIE_KEY = 'collective.weather.current_city'

        city = self.weather_utility.get_current_city()
        expected_city = {'id': u'Cordoba',
                         'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'yahoo'}

        self.assertEqual(city, expected_city)

        self.request.cookies[COOKIE_KEY] = 'Los Angeles'

        city = self.weather_utility.get_current_city()
        expected_city = {'id': u'Los Angeles',
                         'location_id': u'USCA0638',
                         'name': u'Los Angeles, California',
                         'type': 'yahoo'}

        self.assertEqual(city, expected_city)

        self.request.cookies[COOKIE_KEY] = 'Los Angeles5'

        city = self.weather_utility.get_current_city()
        expected_city = {'id': u'Cordoba',
                         'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'yahoo'}

        self.assertEqual(city, expected_city)

    def test_update_specific_weather_info(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IWeatherSettings)
        settings.units = 'metric'

        # What we first do is replace all locations created from the registry, with new values
        old_locations = deepcopy(settings.location_ids)
        settings.location_ids = [
            u'Cordoba|Cordoba, Argentina|ARCA0024',
            u'Los Angeles|Los Angeles, California|USCA0639',
            u'New weather|New weather|NEW124',
            u'New weather2|New weather|NEW125',
        ]
        # And reset any existing weather info
        self.weather_utility.weather_info = {}

        # Update weather info for Los Angeles
        self.weather_utility.update_weather_info('Los Angeles')

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-10\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Now, for New weather2
        self.weather_utility.update_weather_info('New weather2')

        expected_values = {u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-10\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'New weather2': {'conditions': u'Snowing',
                                             'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif',
                                             'temp': u'-20\xbaC'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Now, if i ask for an invalid city, i should get for the first one
        self.weather_utility.update_weather_info('New weather3')

        expected_values = {u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'10\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-10\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'New weather2': {'conditions': u'Snowing',
                                             'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif',
                                             'temp': u'-20\xbaC'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Finally, ask for New weather
        self.weather_utility.update_weather_info('New weather')

        expected_values = {u'Cordoba': {'conditions': u'Windy',
                                        'temp': u'10\xbaC',
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'Los Angeles': {'conditions': u'Snowing',
                                            'temp': u'-10\xbaC',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif'},
                           u'New weather': {'conditions': u'Snowing',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif',
                                            'temp': u'-20\xbaC'},
                           u'New weather2': {'conditions': u'Snowing',
                                             'icon': u'http://l.yimg.com/a/i/us/we/52/34.gif',
                                             'temp': u'-20\xbaC'}}

        wi = self.weather_utility.get_weather_info()

        actual_values = dict([(i, wi[i]['weather']) for i in wi])

        self.assertEqual(actual_values, expected_values)

        # Restore original values
        settings.location_ids = old_locations
        # And reset any existing weather info
        self.weather_utility.weather_info = {}
