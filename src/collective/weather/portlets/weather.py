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
from zope.schema.interfaces import IVocabularyFactory


class IWeatherPortlet(IPortletDataProvider):
    '''A weather portlet.
    '''

    header = schema.TextLine(
        title=_(u'Portlet header'),
        description=_(u'Title of the rendered portlet.'),
        required=True,
    )

    location = schema.Choice(
        title=_(u'Location'),
        description=_(u'Choose one of the preconfigured locations.'),
        required=True,
        vocabulary='collective.weather.Locations',
    )


class Assignment(base.Assignment):
    '''Portlet assignment.
    '''

    implements(IWeatherPortlet)

    header = u''
    location = u''

    def __init__(self, header=u'', location=u''):
        self.header = header
        self.location = location

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
        factory = getUtility(
            IVocabularyFactory, name='collective.weather.Locations')
        vocab = factory(self.context)
        self.current_city = None
        if self.data.location in vocab:
            location = vocab.by_value[self.data.location]
            self.current_city = {'location_id': location.value, 'name': location.title}

        self.weather_info = None
        if self.current_city is not None:
            weather_utility.update_weather_info(self.current_city['location_id'])
            self.weather_info = weather_utility.get_weather_info(self.current_city)


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

    label = _(u'Edit Weather Portlet')
