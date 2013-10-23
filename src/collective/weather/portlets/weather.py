# -*- coding: utf-8 -*-

from collective.weather import _
from collective.weather.interfaces import IWeatherUtility
from plone.app.portlets.portlets import base
from plone.app.portlets.browser.formhelper import NullAddForm
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from zope.interface import implements


class IWeatherPortlet(IPortletDataProvider):
    """A weather portlet.
    """


class Assignment(base.Assignment):
    """Portlet assignment.
    """

    implements(IWeatherPortlet)

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u'Weather portlet')


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('weather.pt')

    def update(self):
        weather_utility = getUtility(IWeatherUtility)
        self.weather_info = weather_utility.get_weather_info()


class AddForm(NullAddForm):
    """Portlet add form.
    """

    def create(self):
        return Assignment()
