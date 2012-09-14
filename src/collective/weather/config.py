# -*- coding: utf-8 -*-

from datetime import timedelta

PROJECTNAME = 'collective.weather'
COOKIE_KEY = 'collective.weather.%s'

# Time that should pass before fetching new weather information.
TIME_THRESHOLD = timedelta(minutes=30)