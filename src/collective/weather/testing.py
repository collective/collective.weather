# -*- coding: utf-8 -*-

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import pywapi
import urllib2


def get_weather_from_yahoo(location_id, units='metric'):
    if location_id == 'ARCA0023':
        result = {'condition': {'text': u'Windy',
                                'temp': u'20',
                                'code': u'34'}
                  }

    if location_id == 'USCA0638':
        result = {'condition': {'text': u'Snowing',
                                'temp': u'-8',
                                'code': u'34'}
                  }

    if location_id == 'NEW123':
        result = {'condition': {'text': u'Snowing',
                                'temp': u'-8',
                                'code': u'34'}
                  }

    if location_id == 'NEW123-invalid':
        result = {'condition': {'temp': u'-8',
                                'code': u'34'}
                  }

    if location_id == 'ARBA0023-urllib-exception':
        raise urllib2.URLError('')

    if location_id == 'ARBA0023-exception':
        raise ValueError

    if location_id == 'ARCA0024':
        result = {'condition': {'text': u'Windy',
                                'temp': u'10',
                                'code': u'34'}
                  }

    if location_id == 'USCA0639':
        result = {'condition': {'text': u'Snowing',
                                'temp': u'-10',
                                'code': u'34'}
                  }

    if location_id == 'NEW124':
        result = {'condition': {'text': u'Snowing',
                                'temp': u'-20',
                                'code': u'34'}
                  }
    if location_id == 'NEW125':
        result = {'condition': {'text': u'Snowing',
                                'temp': u'-20',
                                'code': u'34'}
                  }

    return result


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        pywapi.get_weather_from_yahoo = get_weather_from_yahoo
        import collective.weather
        self.loadZCML(package=collective.weather)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.weather:default')
        self.applyProfile(portal, 'collective.weather:test_fixture')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.weather:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.weather:Functional',
)
