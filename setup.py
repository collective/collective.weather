# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup


version = '1.0a4'
description = 'A Plone package to display the current weather at selected locations inside a portlet or viewlet.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='collective.weather',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.1',
          'Framework :: Plone :: 4.2',
          'Framework :: Plone :: 4.3',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='api google noaa plone weather yahoo',
      author='OpenMultimedia',
      author_email='contacto@openmultimedia.biz',
      url='https://github.com/collective/collective.weather',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'plone.api',
          'plone.app.layout',
          'plone.app.portlets',
          'plone.app.registry',
          'plone.directives.form',
          'plone.i18n',
          'plone.portlets',
          'plone.registry',
          'Products.CMFCore',
          'Products.CMFPlone >=4.1',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'AccessControl',
              'plone.app.testing',
              'plone.browserlayer',
              'plone.testing',
              'unittest2',
          ],
      },
      )
