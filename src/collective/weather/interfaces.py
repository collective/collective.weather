# -*- coding: utf-8 -*-

from collective.weather import _
from collective.weather.config import UNIT_SYSTEMS
from collective.weather.config import WEATHER_APIS
from plone.directives import form
from zope import schema
from zope.interface import Interface


class IWeatherLayer(Interface):
    """A layer specific for this add-on product.
    """


class IWeatherUtility(Interface):
    """Interface for the weather utility
    """


class IWeatherSettings(form.Schema):
    """Settings for the collective.weather package.
    """

    weather_api = schema.Choice(
        title=_(u'Weather service to be used'),
        default='yahoo',
        required=True,
        vocabulary=WEATHER_APIS,
    )

    location_ids = schema.List(
        title=_(u'Available locations'),
        description=_(u'Enter here all available locations that will be '
                      u'shown in the locations drop down. Format: id|name|location_id. '
                      u'Check the <a href="https://github.com/collective/collective.weather#id9">package documentation</a> '
                      u'for further information on how to find the location_id.'),
        value_type=schema.TextLine(),
        required=True,
        default=[],
    )

    units = schema.Choice(
        title=_(u'Units'),
        description=_(u'System of units to be used: metric or imperial.'),
        required=True,
        default='metric',
        vocabulary=UNIT_SYSTEMS,
    )

    show_viewlet = schema.Bool(
        title=_(u'Show weather viewlet?'),
        description=_(u'Defines if the weather viewlet will be shown or not.'),
        required=True,
        default=False,
    )
