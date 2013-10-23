# -*- coding: utf-8 -*-

from collective.weather.testing import INTEGRATION_TESTING
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from zope.component import getUtility

import unittest2 as unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.weather:default'
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        """Get one of the upgrade steps.

        Keyword arguments:
        title -- the title used to register the upgrade step
        """
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        Keyword arguments:
        step -- the step we want to run
        """
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    def _how_many_upgrades_to_do(self):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class Upgrade1to2TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1', u'2')

    def test_upgrade_to_2_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(version >= self.to_version)
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_code_clean_up(self):
        # check if the upgrade step is registered
        title = u'code_clean_up'
        description = u'Remove all Google Weather related code.'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)
        self.assertEqual(step['description'], description)

        # simulate state on previous version
        registry = getUtility(IRegistry)
        prefix = 'collective.weather.browser.interfaces.IGoogleWeatherSchema.'
        records = [
            prefix + 'use_google',
            prefix + 'google_location_ids',
            prefix + 'google_language',
            prefix + 'google_units',
        ]

        for r in records:
            registry.records[r] = Record(field.TextLine(title=u'Test'))
            self.assertIn(r, registry)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)

        for r in records:
            self.assertNotIn(r, registry)
