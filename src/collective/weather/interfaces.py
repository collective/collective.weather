# -*- coding: utf-8 -*-

from zope.interface import Interface


class IWeatherLayer(Interface):
    """ A layer specific for this add-on product.
    """


class IWeatherUtility(Interface):
    """
    Interface for the weather utility
    """