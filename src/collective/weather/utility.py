
from AccessControl import ClassSecurityInfo

from zope.interface import classProvides
from zope.interface import implements

from zope.schema.fieldproperty import FieldProperty

from collective.weather.browser.interfaces import IWeatherSchema
from collective.weather.browser.interfaces import IGoogleWeatherSchema
from collective.weather.browser.interfaces import IYahooWeatherSchema
from collective.weather.browser.interfaces import INoaaWeatherSchema

# def form_adapter(context):
#     """Form Adapter"""
#     return getUtility(IWeatherSchema)


class Weather(SimpleItem):
    """Weather Utility"""
    implements(IWeatherSchema)
    classProvides(
        IGoogleWeatherSchema,
        IYahooWeatherSchema,
        INoaaWeatherSchema
        )

    security = ClassSecurityInfo()

    use_google = FieldProperty(IGoogleWeatherSchema('use_google'))
    google_location_ids = FieldProperty(IGoogleWeatherSchema('google_location_ids'))
    google_language = FieldProperty(IGoogleWeatherSchema('google_language'))
    google_units = FieldProperty(IGoogleWeatherSchema('google_units'))
    use_yahoo = FieldProperty(IYahooWeatherSchema('use_yahoo'))
    yahoo_location_ids = FieldProperty(IYahooWeatherSchema('yahoo_location_ids'))
    yahoo_units = FieldProperty(IYahooWeatherSchema('yahoo_units'))
    use_noaa = FieldProperty(INoaaWeatherSchema('use_noaa'))
    noaa_location_ids = FieldProperty(INoaaWeatherSchema('noaa_location_ids'))
