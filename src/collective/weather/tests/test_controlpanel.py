# -*- coding: utf-8 -*-

from collective.weather.interfaces import IWeatherSettings
from collective.weather.config import PROJECTNAME
from collective.weather.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view('weather-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@weather-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('WeatherSettings', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('WeatherSettings', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IWeatherSettings)

    def test_weather_api_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'weather_api'))
        self.assertEqual(self.settings.weather_api, 'testprovider')

    def test_weather_api_key_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'weather_api_key'))
        self.assertFalse(self.settings.weather_api_key)

    def test_location_ids_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'location_ids'))
        # as defined in the test fixture
        expected = [
            u'ARCA0023|Cordoba, Argentina',
            u'USCA0638|Los Angeles, California'
        ]
        self.assertEqual(self.settings.location_ids, expected)

    def test_units_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'units'))
        self.assertEqual(self.settings.units, u'metric')

    def test_show_viewlet_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'show_viewlet'))
        # as defined in the test fixture
        self.assertEqual(self.settings.show_viewlet, True)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])

        prefix = 'collective.weather.interfaces.IWeatherSettings.'
        records = [
            prefix + 'weather_api',
            prefix + 'weather_api_key',
            prefix + 'location_ids',
            prefix + 'units',
            prefix + 'show_viewlet',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
