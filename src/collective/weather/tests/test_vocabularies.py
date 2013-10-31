# -*- coding: utf-8 -*-

from collective.weather.testing import INTEGRATION_TESTING
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_locations_vocabulary(self):
        name = 'collective.weather.Cities'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util)
        locations = util(self.portal)
        # as defined in the test fixture
        self.assertEqual(len(locations), 2)
        self.assertIn('Cordoba', locations)
        self.assertIn(u'Los Angeles', locations)
