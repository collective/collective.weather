from zope.component import getUtility, getMultiAdapter
from zope.site.hooks import setHooks, setSite

from Products.GenericSetup.utils import _getDottedName

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from collective.weather.portlets import weather
from plone.app.portlets.tests.base import PortletsTestCase

import unittest


class TestPortlet(PortletsTestCase):

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)
        self.setRoles(('Manager', ))

    @unittest.expectedFailure
    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='collective.weather.portlets.weather')
        self.assertEquals(portlet.addview, 'collective.weather.portlets.weather')

    @unittest.expectedFailure
    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='collective.weather.portlets.weather')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn',
                           'plone.app.portlets.interfaces.IDashboard'],
                          registered_interfaces)

    def testInterfaces(self):
        portlet = weather.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    @unittest.expectedFailure
    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='collective.weather.portlets.weather')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # This is a NullAddForm - calling it does the work
        addview()

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], weather.Assignment))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = weather.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, weather.Renderer))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    return suite
