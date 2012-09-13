# -*- coding: utf-8 -*-

from zope.component import getUtility

from zope.interface import alsoProvides

from z3c.form import field
from z3c.form import group

from plone.app.registry.browser import controlpanel

from plone.fieldsets.fieldsets import FormFieldsets

from plone.registry.interfaces import IRegistry

from collective.z3cform.widgets.enhancedtextlines import EnhancedTextLinesFieldWidget

from collective.weather.browser.interfaces import IWeatherControlPanelForm
from collective.weather.browser.interfaces import IGoogleWeatherSchema
from collective.weather.browser.interfaces import IYahooWeatherSchema
from collective.weather.browser.interfaces import INoaaWeatherSchema
from collective.weather.browser.interfaces import IWeatherSchema

from collective.weather import _


class GoogleGroup(group.Group):
    label = _(u"Google")
    description = _("""WARNING: Google Weather is not working at the moment.""")
    fields = field.Fields(IGoogleWeatherSchema)


class YahooGroup(group.Group):
    label = _(u"Yahoo")
    fields = field.Fields(IYahooWeatherSchema)


class NoaaGroup(group.Group):
    label = _(u"NOAA")
    description = _("""WARNING: NOAA Weather is not working at the moment.""")
    fields = field.Fields(INoaaWeatherSchema)


class WeatherControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IWeatherSchema

    label = _("Weather Setup")
    description = _("""Lets you configure several weather locations""")

    fields = IYahooWeatherSchema

    groups = NoaaGroup, GoogleGroup

    def getContent(self):
        return AbstractRecordsProxy(self.schema)

    # def updateFields(self):
    #     super(WeatherControlPanelEditForm, self).updateFields()
    #     self.fields['google_location_ids'].widgetFactory = EnhancedTextLinesFieldWidget
    #     self.groups[0].fields['yahoo_location_ids'].widgetFactory = EnhancedTextLinesFieldWidget
    #     self.groups[1].fields['noaa_location_ids'].widgetFactory = EnhancedTextLinesFieldWidget

    # def updateWidgets(self):
    #     super(WeatherControlPanelEditForm, self).updateWidgets()
    #     self.widgets['available_sections'].rows = 8
    #     self.widgets['available_sections'].style = u'width: 30%;'


class WeatherControlPanel(controlpanel.ControlPanelFormWrapper):
    form = WeatherControlPanelEditForm


class AbstractRecordsProxy(object):
    """Multiple registry schema proxy.

    This class supports schemas that contain derived fields. The
    settings will be stored with respect to the individual field
    interfaces.
    """

    def __init__(self, schema):
        state = self.__dict__
        state["__registry__"] = getUtility(IRegistry)
        state["__proxies__"] = {}
        state["__schema__"] = schema
        alsoProvides(self, schema)

    def __getattr__(self, name):
        try:
            field = self.__schema__[name]
        except KeyError:
            raise AttributeError(name)
        else:
            proxy = self._get_proxy(field.interface)
            return getattr(proxy, name)

    def __setattr__(self, name, value):
        try:
            field = self.__schema__[name]
        except KeyError:
            self.__dict__[name] = value
        else:
            proxy = self._get_proxy(field.interface)
            return setattr(proxy, name, value)

    def __repr__(self):
        return "<AbstractRecordsProxy for %s>" % self.__schema__.__identifier__

    def _get_proxy(self, interface):
        proxies = self.__proxies__
        return proxies.get(interface) or \
               proxies.setdefault(interface,
                                  self.__registry__.forInterface(interface))
