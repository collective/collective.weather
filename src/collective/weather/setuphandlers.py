# -*- coding:utf-8 -*-

from collective.weather.config import PROJECTNAME
from Products.CMFCore.utils import getToolByName

import logging


def upgrade_to_2(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger(PROJECTNAME)

    profile = 'profile-collective.weather:upgrade_to_2'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)
