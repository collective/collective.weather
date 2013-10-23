# -*- coding: utf-8 -*-

from collective.weather.browser.interfaces import INoaaWeatherSchema
from collective.weather.browser.interfaces import IYahooWeatherSchema
from collective.weather.config import PROJECTNAME
from collective.weather.testing import INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest2 as unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name='weather-controlpanel')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@weather-controlpanel')

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


class YahooRegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IYahooWeatherSchema)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_use_yahoo_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'use_yahoo'))
        self.assertEqual(self.settings.use_yahoo, True)

    def test_yahoo_location_ids_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'yahoo_location_ids'))
        existing_data = [u'Cordoba|Cordoba, Argentina|ARCA0023',
                         u'Los Angeles|Los Angeles, California|USCA0638']

        self.assertEqual(self.settings.yahoo_location_ids, existing_data)

    def test_yahoo_units_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'yahoo_units'))
        self.assertEqual(self.settings.yahoo_units, u'metric')

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])

        prefix = 'collective.weather.browser.interfaces.IYahooWeatherSchema.'
        records = [
            prefix + 'use_yahoo',
            prefix + 'yahoo_location_ids',
            prefix + 'yahoo_units',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)


class NoaaRegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(INoaaWeatherSchema)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_use_noaa_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'use_noaa'))
        self.assertEqual(self.settings.use_noaa, False)

    def test_noaa_location_ids_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'noaa_location_ids'))
        self.assertEqual(self.settings.noaa_location_ids, [])

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])

        prefix = 'collective.weather.browser.interfaces.INoaaWeatherSchema.'
        records = [
            prefix + 'use_noaa',
            prefix + 'noaa_location_ids',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
