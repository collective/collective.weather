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
        description=_(
            u'help_weather_api',
            default=u''),
        default='yahoo',
        required=True,
        vocabulary=WEATHER_APIS,
    )

    location_ids = schema.List(
        title=_(u'Available locations'),
        description=_(
            u'help_location_ids',
            default=u'Enter here all available locations that will be '
                    u'available. Format: id|name|location_id. Check the '
                    u'<a href="https://github.com/collective/collective.weather#finding-locations">package documentation</a> '
                    u'for further information on how to find ids.'),
        value_type=schema.TextLine(),
        required=True,
        default=[],
    )

    units = schema.Choice(
        title=_(u'Units'),
        description=_(
            u'help_units',
            default=u'System of units to be used: metric or imperial. '
                    u'Metric system uses degrees Celsius. '
                    u'Imperial system uses degrees Fahrenheit.'),
        required=True,
        default='metric',
        vocabulary=UNIT_SYSTEMS,
    )

    show_viewlet = schema.Bool(
        title=_(u'Show weather viewlet?'),
        description=_(
            u'help_show_viewlet',
            default=u'Defines whether or not the weather viewlet will be '
                    u'shown site wide.'),
        required=True,
        default=False,
    )
