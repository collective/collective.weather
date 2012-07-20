
from AccessControl import ClassSecurityInfo

from zope.component import getUtility

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

    use_google = FieldProperty(IGoogleWeatherSchema("use_google"))
    g_locations_id = FieldProperty(IGoogleWeatherSchema("g_locations_id"))
    g_hl = FieldProperty(IGoogleWeatherSchema("g_hl"))
    g_units = FieldProperty(IGoogleWeatherSchema("g_units"))
    use_yahoo = FieldProperty(IYahooWeatherSchema("use_yahoo"))
    y_locations_id = FieldProperty(IYahooWeatherSchema("y_locations_id"))
    y_units = FieldProperty(IYahooWeatherSchema("y_units"))
    use_noaa = FieldProperty(INoaaWeatherSchema("use_noaa"))
    n_locations_id = FieldProperty(INoaaWeatherSchema("n_locations_id"))


