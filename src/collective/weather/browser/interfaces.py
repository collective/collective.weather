from zope.interface import Interface

from zope import schema

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from plone.directives import form

from collective.z3cform.widgets.enhancedtextlines import EnhancedTextLinesFieldWidget

from collective.weather import _

units_vocab = SimpleVocabulary(
    [SimpleTerm(value=u'metric', title=_(u'Metric')),
     SimpleTerm(value=u'imperial', title=_(u'Imperial'))])


class IGoogleWeatherSchema(form.Schema):
    """ 
    Configurations for getting weather information from Google 
    """

    use_google = schema.Bool(title=_(u"Use Google weather service"))

    form.widget(g_locations_id=EnhancedTextLinesFieldWidget)
    g_locations_id = schema.List(title=_(u"Available options"),
                                 description=_(u"Enter here all available locations that will be shown in the locations drop down."),
                                 value_type= schema.TextLine(),
                                 default=[],
                                 required=False)

    g_hl = schema.TextLine(title=_(u"Language"),
                           description=_(u"Enter the language code to show the content."),
                           required=False)

    g_units = schema.Choice(title=_(u'Units'),
                            description=_(u"Units to show the results."),
                            default='metric',
                            required=True,
                            source=units_vocab)


class IYahooWeatherSchema(form.Schema):
    """ 
    Configurations for getting weather information from Yahoo
    """

    use_yahoo = schema.Bool(title=_(u"Use Yahoo weather service"))

    form.widget(y_locations_id=EnhancedTextLinesFieldWidget)
    y_locations_id = schema.List(title=_(u"Available options"),
                                 description=_(u"Enter here all available locations that "
                                                "will be shown in the locations drop down."
                                                "Check http://code.google.com/p/python-weather-api/#Yahoo!_Weather for further information."),
                                 value_type= schema.TextLine(),
                                 default=[],
                                 required=False)

    y_units = schema.Choice(title=_(u'Units'),
                            description=_(u"Units to show the results."),
                            default='metric',
                            required=True,
                            source=units_vocab)


class INoaaWeatherSchema(form.Schema):
    """ 
    Configurations for getting weather information from NOAA
    """

    use_noaa = schema.Bool(title=_(u"Use NOAA weather service"))

    form.widget(n_locations_id=EnhancedTextLinesFieldWidget)
    n_locations_id = schema.List(title=_(u"Available options"),
                                 description=_(u"Enter here all available locations that "
                                                "will be shown in the locations drop down. "
                                                "Check http://code.google.com/p/python-weather-api/#NOAA for further information."),
                                 value_type= schema.TextLine(),
                                 default=[],
                                 required=False)


class IWeatherSchema(IGoogleWeatherSchema, IYahooWeatherSchema, INoaaWeatherSchema):
    """
    """

class IWeatherControlPanelForm(Interface):
    """
    Control panel used to manage weather configurations
    """
    