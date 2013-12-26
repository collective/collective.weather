# -*- coding: utf-8 -*-

from collective.weather.testing import FUNCTIONAL_TESTING
from plone.testing import layered

import os
import doctest
import unittest2 as unittest

dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.endswith('.txt')]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(t), layer=FUNCTIONAL_TESTING)
        for t in tests
    ])
    return suite
