from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CollectiveWeather(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.weather
        xmlconfig.file('configure.zcml',
                       collective.weather,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.weather:default')

COLLECTIVE_WEATHER_FIXTURE = CollectiveWeather()
COLLECTIVE_WEATHER_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_WEATHER_FIXTURE, ),
                       name="CollectiveWeather:Integration")