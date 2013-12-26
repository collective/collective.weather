# -*- coding: utf-8 -*-

from collective.weather.config import PROJECTNAME
from collective.weather.portlets import weather
from plone import api
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import queryUtility


def uninstall(portal, reinstall=False):
    if not reinstall:
        profile = 'profile-%s:uninstall' % PROJECTNAME
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        remove_weather_portlets(portal)
        return 'Ran all uninstall steps.'


def remove_weather_portlets(portal):
    """Remove all weather portlets from any content of the site.

    See: http://developer.plone.org/functionality/portlets.html#walking-through-every-portlet-on-the-site
    """

    # Get all portlet assignable content
    all_content = portal.portal_catalog(show_inactive=True)
    all_content = [content.getObject() for content in all_content]
    all_content = list(all_content) + [portal]

    for content in all_content:
        for manager_name in ['plone.leftcolumn', 'plone.rightcolumn']:
            manager = queryUtility(IPortletManager, name=manager_name, context=content)
            if not manager:
                continue

            mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)

            for id, assignment in mapping.items():
                if isinstance(assignment, weather.Assignment):
                    del mapping[id]
