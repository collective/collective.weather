# -*- coding: utf-8 -*-

from collective.weather.testing import FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest2 as unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/functional.txt',
                                     package='collective.weather'),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
