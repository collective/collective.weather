# -*- coding: utf-8 -*-

from collective.weather.portlets import weather
from collective.weather.testing import INTEGRATION_TESTING
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from Products.GenericSetup.utils import _getDottedName
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest2 as unittest


class PortletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.name = 'collective.weather.portlets.weather'

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name=self.name)
        self.assertEqual(portlet.addview, self.name)

    def test_registered_interfaces(self):
        portlet = getUtility(IPortletType, name=self.name)
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        expected = [
            'plone.app.portlets.interfaces.IColumn',
            'plone.app.portlets.interfaces.IDashboard',
        ]

        self.assertItemsEqual(registered_interfaces, expected)

    def test_interfaces(self):
        portlet = weather.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name=self.name)
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')

        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={'header': u'Weather', 'location': u'ARCA0023'})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], weather.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()

        mapping['test'] = weather.Assignment()
        editview = getMultiAdapter(
            (mapping['test'], self.request), name='edit')
        self.assertTrue(isinstance(editview, weather.EditForm))

    def test_renderer(self):
        context = self.portal
        request = self.request
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = weather.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, weather.Renderer))


class RenderTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        assignment = weather.Assignment(header=u'Weather', location=u'ARCA0023')

        r = self.renderer(assignment=assignment)
        r = r.__of__(self.portal)
        r.update()

        # XXX: at this point the weather information has already been
        #      updated by another test; we need to isolate this
        # at first rendering no weather information is available
        # self.assertIn(u'Cordoba, Argentina', r.render())
        # self.assertIn(u'No weather information', r.render())

        # call the update weather view and test again
        # self.portal.unrestrictedTraverse('@@update-weather')()
        self.assertIn(u'Cordoba, Argentina', r.render())
        self.assertIn(u'Windy', r.render())
        self.assertIn(u'20\xb0C', r.render())
