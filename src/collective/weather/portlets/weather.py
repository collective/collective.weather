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
    """ A weather portlet
    """

    time_to_live = schema.Float(
        title=_(u"Time to live"),
        description=_("After the specified minutes, the portlet will refresh its data"),
        required=True)


class Assignment(base.Assignment):
    """ Portlet assignment.
    """

    implements(IWeatherPortlet)

    def __init__(self, time_to_live=30):
        self.time_to_live = time_to_live

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Weather portlet")


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('weather.pt')

    def update(self):
        weather_utility = getUtility(IWeatherUtility)
        self.weather_info = weather_utility.get_weather_info()


class AddForm(base.AddForm):
    """Portlet add form.
    """

    form_fields = form.Fields(IWeatherPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """

    form_fields = form.Fields(IWeatherPortlet)
