# -*- coding: utf-8 -*-

from collective.weather import _
from collective.weather.interfaces import IWeatherUtility
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements


class IWeatherPortlet(IPortletDataProvider):
    '''A weather portlet.
    '''

    header = schema.TextLine(
        title=_(u'Portlet header'),
        description=_(u'Title of the rendered portlet'),
        required=True)

    city = schema.Choice(
        title=_(u'City'),
        description=_(u'Choose one of the preconfigured cities'),
        required=True,
        vocabulary='collective.weather.Cities')


class Assignment(base.Assignment):
    '''Portlet assignment.
    '''

    implements(IWeatherPortlet)

    header = u''
    city = u''

    def __init__(self, header=u'', city=u''):
        self.header = header
        self.city = city

    @property
    def title(self):
        '''This property is used to give the title of the portlet in the
        'manage portlets' screen.
        '''
        return self.header


class Renderer(base.Renderer):
    '''Portlet renderer.
    '''

    render = ViewPageTemplateFile('weather.pt')

    def update(self):
        weather_utility = getUtility(IWeatherUtility)
        self.weather_info = weather_utility.get_weather_info()


class AddForm(base.AddForm):
    '''Portlet add form.
    '''

    form_fields = form.Fields(IWeatherPortlet)

    label = _(u'Add Weather Portlet')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    '''Portlet edit form.
    '''

    form_fields = form.Fields(IWeatherPortlet)

    label = _(u'Add Weather Portlet')
