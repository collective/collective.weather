# -*- coding: utf-8 -*-

from collective.weather import _
from collective.weather.interfaces import IWeatherSettings
from plone.app.registry.browser import controlpanel


class WeatherControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IWeatherSettings

    label = _('Weather Setup')
    description = _('Settings for the collective.weather package')


class WeatherSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = WeatherControlPanelEditForm
