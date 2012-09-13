# -*- coding: utf-8 -*-

from zope.interface import Interface

from zope import schema

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from plone.directives import form

from collective.weather import _

units_vocab = SimpleVocabulary(
    [SimpleTerm(value=u'metric', title=_(u'Metric')),
     SimpleTerm(value=u'imperial', title=_(u'Imperial'))])


class IGoogleWeatherSchema(form.Schema):
    """
    Configurations for getting weather information from Google
    """

    use_google = schema.Bool(title=_(u"Use Google Weather service"),
        default=False,
        )

    form.widget(google_location_ids="collective.z3cform.widgets.enhancedtextlines.EnhancedTextLinesFieldWidget")
    google_location_ids = schema.List(title=_(u"Available options"),
                                 description=_(u"Enter here all available locations that will be shown in the locations drop down. Format: id|name|location_id."),
                                 value_type=schema.TextLine(),
                                 default=[],
                                 required=False)

    google_language = schema.TextLine(title=_(u"Language"),
                           description=_(u"Enter the language code to show the content."),
                           required=False)

    google_units = schema.Choice(title=_(u'Units'),
                            description=_(u"Units to show the results."),
                            default='metric',
                            required=False,
                            source=units_vocab)


class IYahooWeatherSchema(form.Schema):
    """
    Configurations for getting weather information from Yahoo
    """

    use_yahoo = schema.Bool(title=_(u"Use Yahoo! Weather service"),
        default=False,
        )

    form.widget(yahoo_location_ids="collective.z3cform.widgets.enhancedtextlines.EnhancedTextLinesFieldWidget")
    yahoo_location_ids = schema.List(title=_(u"Available options"),
                                 description=_(u"Enter here all available locations that "
                                                "will be shown in the locations drop down. Format: id|name|location_id. "
                                                "Check http://code.google.com/p/python-weather-api/#Yahoo!_Weather for further information."),
                                 value_type=schema.TextLine(),
                                 default=[],
                                 required=False)

    yahoo_units = schema.Choice(title=_(u'Units'),
                            description=_(u"Units to show the results."),
                            default='metric',
                            required=False,
                            source=units_vocab)


class INoaaWeatherSchema(form.Schema):
    """
    Configurations for getting weather information from NOAA
    """

    use_noaa = schema.Bool(title=_(u"Use NOAA weather service (XXX: not yet implemented)"),
        default=False,
        )

    form.widget(noaa_location_ids="collective.z3cform.widgets.enhancedtextlines.EnhancedTextLinesFieldWidget")
    noaa_location_ids = schema.List(title=_(u"Available options"),
                                 description=_(u"Enter here all available locations that "
                                                "will be shown in the locations drop down. Format: id|name|location_id. "
                                                "Check http://code.google.com/p/python-weather-api/#NOAA for further information."),
                                 value_type=schema.TextLine(),
                                 default=[],
                                 required=False)


class IWeatherSchema(IGoogleWeatherSchema, IYahooWeatherSchema, INoaaWeatherSchema):
    """
    """


class IWeatherControlPanelForm(Interface):
    """
    Control panel used to manage weather configurations
    """
