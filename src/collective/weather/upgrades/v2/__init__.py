# -*- coding: utf-8 -*-

from collective.weather.config import PROJECTNAME
from Products.CMFCore.utils import getToolByName

import logging


def code_clean_up(context, logger=None):
    """Remove all Google Weather related code.
    """
    if logger is None:
        logger = logging.getLogger(PROJECTNAME)

    profile = 'profile-collective.weather.upgrades.v2:default'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)
