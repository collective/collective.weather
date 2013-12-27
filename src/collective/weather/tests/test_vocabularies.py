# -*- coding: utf-8 -*-

from collective.weather.testing import INTEGRATION_TESTING
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest2 as unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_locations_vocabulary(self):
        name = 'collective.weather.Locations'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util)
        locations = util(self.portal)
        # as defined in the test fixture
        self.assertEqual(len(locations), 2)
        self.assertIn('ARCA0023', locations)
        self.assertIn('USCA0638', locations)

    def test_providers_vocabulary(self):
        name = 'collective.weather.Providers'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util)
        providers = util(self.portal)
        # collective.weather already comes with 3 providers
        self.assertTrue(len(providers) >= 3)
        self.assertIn(u'forecast.io', providers)
        self.assertIn(u'yahoo', providers)
        self.assertIn(u'wunderground', providers)
