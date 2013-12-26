# -*- coding: utf-8 -*-

from collective.weather import _
from datetime import timedelta
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

PROJECTNAME = 'collective.weather'
COOKIE_KEY = 'collective.weather.%s'

# Time that should pass before fetching new weather information.
TIME_THRESHOLD = timedelta(minutes=30)

UNIT_SYSTEMS = SimpleVocabulary([
    SimpleTerm(value=u'metric', title=_(u'Metric')),
    SimpleTerm(value=u'imperial', title=_(u'Imperial')),
])
