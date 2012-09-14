# -*- coding: utf-8 -*-

from datetime import timedelta

from copy import deepcopy
import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from collective.weather.config import PROJECTNAME

from collective.weather.interfaces import IWeatherUtility

from collective.weather.browser.interfaces import IGoogleWeatherSchema
from collective.weather.browser.interfaces import INoaaWeatherSchema
from collective.weather.browser.interfaces import IYahooWeatherSchema
from collective.weather.testing import INTEGRATION_TESTING


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
        yahoo_settings = registry.forInterface(IYahooWeatherSchema)
        old_ids = deepcopy(yahoo_settings.yahoo_location_ids)

        expected_values = [{'id': u'Cordoba',
                            'location_id': u'ARCA0023',
                            'name': u'Cordoba, Argentina',
                            'type': 'yahoo'},
                           {'id': u'Los Angeles',
                            'location_id': u'USCA0638',
                            'name': u'Los Angeles, California',
                            'type': 'yahoo'}]

        actual_values = self.weather_utility.get_cities_list()

        self.assertEquals(actual_values, expected_values)

        # We add a new city to the registry
        yahoo_settings.yahoo_location_ids.append(u"New city|New city, Test|LALA1212")

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

        self.assertEquals(actual_values, expected_values)

        # Finally, we add a malformed value to the list
        yahoo_settings.yahoo_location_ids.append("My city")
        
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

        self.assertEquals(actual_values, expected_values)

        #restore old values
        yahoo_settings.yahoo_location_ids = old_ids

    def test_update_weather_info(self):
        registry = getUtility(IRegistry)
        yahoo_settings = registry.forInterface(IYahooWeatherSchema)

        # Update weather info
        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing', 
                                            'temp': u'-8\xbaC', 
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}, 
                           u'Cordoba': {'conditions': u'Windy', 
                                        'temp': u'20\xbaC', 
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEquals(actual_values, expected_values)

        # Now, we add a new city
        old_locations = deepcopy(yahoo_settings.yahoo_location_ids)
        yahoo_settings.yahoo_location_ids.append(u"New weather|New weather|NEW123")

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing', 
                                            'temp': u'-8\xbaC', 
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}, 
                           u'Cordoba': {'conditions': u'Windy', 
                                        'temp': u'20\xbaC', 
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'},
                           u'New weather': {'conditions': u'Snowing',
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif',
                                            'temp': u'-8\xbaC'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEquals(actual_values, expected_values)

        # If we remove the new city, then we should no longer get it
        yahoo_settings.yahoo_location_ids = old_locations

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing', 
                                            'temp': u'-8\xbaC', 
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}, 
                           u'Cordoba': {'conditions': u'Windy', 
                                        'temp': u'20\xbaC', 
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEquals(actual_values, expected_values)

        # We are going to forge weather info into the utility so we simulate invalid returned values and errors
        self.weather_utility.weather_info['New weather'] = {'weather': {'conditions': u'Snowing', 
                                                                        'temp': u'-8\xbaC', 
                                                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        # We create a city with the same name but different location_id, so we can simulate
        # invalid results for an existing city. In this case, it should be removed
        yahoo_settings.yahoo_location_ids.append(u"New weather|New weather|NEW123-invalid")
        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing', 
                                            'temp': u'-8\xbaC', 
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}, 
                           u'Cordoba': {'conditions': u'Windy', 
                                        'temp': u'20\xbaC', 
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEquals(actual_values, expected_values)

        self.weather_utility.weather_info['Buenos Aires'] = {'weather': {'conditions': u'Snowing', 
                                                                        'temp': u'-8\xbaC', 
                                                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        # If we get a urllib exception, then also remove the existing value
        yahoo_settings.yahoo_location_ids.append(u"Buenos Aires|Buenos Aires, Argentina|ARBA0023-urllib-exception")

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing', 
                                            'temp': u'-8\xbaC', 
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}, 
                           u'Cordoba': {'conditions': u'Windy', 
                                        'temp': u'20\xbaC', 
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])
        self.assertEquals(actual_values, expected_values)

        self.weather_utility.weather_info['Los Angeles'] = {'weather': {'conditions': u'Snowing', 
                                                                        'temp': u'-8\xbaC', 
                                                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        # If we get a urllib exception, then also remove the existing value
        yahoo_settings.yahoo_location_ids.append(u"Buenos Aires|Buenos Aires, Argentina|ARBA0023-exception")

        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing', 
                                            'temp': u'-8\xbaC', 
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}, 
                           u'Cordoba': {'conditions': u'Windy', 
                                        'temp': u'20\xbaC', 
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEquals(actual_values, expected_values)

        # Test imperial units
        yahoo_settings.yahoo_units = 'imperial'
        self.weather_utility.weather_info = {}
        self.weather_utility.update_weather_info()

        expected_values = {u'Los Angeles': {'conditions': u'Snowing', 
                                            'temp': u'-8\xbaF', 
                                            'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}, 
                           u'Cordoba': {'conditions': u'Windy', 
                                        'temp': u'20\xbaF', 
                                        'icon': u'http://l.yimg.com/a/i/us/we/52/.gif'}}

        actual_values = dict([(i, self.weather_utility.get_weather_info()[i]['weather']) for i in self.weather_utility.get_weather_info()])

        self.assertEquals(actual_values, expected_values)


    def test_get_city(self):
        city = self.weather_utility.get_city('Cordoba')
        expected_city = {'id': u'Cordoba',
                         'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'yahoo'}

        self.assertEquals(city, expected_city)

        city = self.weather_utility.get_city('Cordoba2')
        expected_city = {}

        self.assertEquals(city, expected_city)

    def test_get_current_city(self):

        COOKIE_KEY = 'collective.weather.top_weather'

        city = self.weather_utility.get_current_city()
        expected_city = {'id': u'Cordoba',
                         'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'yahoo'}

        self.assertEquals(city, expected_city)

        self.request.cookies[COOKIE_KEY] = 'Los Angeles'

        city = self.weather_utility.get_current_city()
        expected_city = {'id': u'Los Angeles',
                         'location_id': u'USCA0638',
                         'name': u'Los Angeles, California',
                         'type': 'yahoo'}

        self.assertEquals(city, expected_city)

        self.request.cookies[COOKIE_KEY] = 'Los Angeles5'

        city = self.weather_utility.get_current_city()
        expected_city = {'id': u'Cordoba',
                         'location_id': u'ARCA0023',
                         'name': u'Cordoba, Argentina',
                         'type': 'yahoo'}

        self.assertEquals(city, expected_city)
