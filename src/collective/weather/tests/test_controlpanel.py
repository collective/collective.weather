# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from collective.weather.config import PROJECTNAME
from collective.weather.browser.interfaces import IGoogleWeatherSchema
from collective.weather.browser.interfaces import INoaaWeatherSchema
from collective.weather.browser.interfaces import IYahooWeatherSchema
from collective.weather.testing import INTEGRATION_TESTING


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='weather-controlpanel')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@weather-controlpanel')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('WeatherSettings' in actions,
                        'control panel was not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('WeatherSettings' not in actions,
                        'control panel was not removed')


class GoogleRegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IGoogleWeatherSchema)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_use_google_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'use_google'))
        self.assertEqual(self.settings.use_google, False)

    def test_google_location_ids_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'google_location_ids'))
        self.assertEqual(self.settings.google_location_ids, [])

    def test_google_language_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'google_language'))
        self.assertEqual(self.settings.google_language, None)

    def test_google_units_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'google_units'))
        self.assertEqual(self.settings.google_units, u'metric')

    def get_record(self, record):
        """ Helper function; it raises KeyError if the record is not in the
        registry.
        """
        prefix = 'collective.weather.browser.interfaces.IGoogleWeatherSchema.'
        return self.registry[prefix + record]

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.get_record, 'use_google')
        self.assertRaises(KeyError, self.get_record, 'google_location_ids')
        self.assertRaises(KeyError, self.get_record, 'google_language')
        self.assertRaises(KeyError, self.get_record, 'google_units')


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

    def get_record(self, record):
        """ Helper function; it raises KeyError if the record is not in the
        registry.
        """
        prefix = 'collective.weather.browser.interfaces.IYahooWeatherSchema.'
        return self.registry[prefix + record]

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.get_record, 'use_yahoo')
        self.assertRaises(KeyError, self.get_record, 'yahoo_location_ids')
        self.assertRaises(KeyError, self.get_record, 'yahoo_units')


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

    def get_record(self, record):
        """ Helper function; it raises KeyError if the record is not in the
        registry.
        """
        prefix = 'collective.weather.browser.interfaces.INoaaWeatherSchema.'
        return self.registry[prefix + record]

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.get_record, 'use_noaa')
        self.assertRaises(KeyError, self.get_record, 'noaa_location_ids')
