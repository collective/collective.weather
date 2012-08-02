from setuptools import setup, find_packages
import os

version = '1.0a1'
description = "A Plone viewlet to display the weather at selected locations."
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.weather',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='api google noaa plone weather yahoo',
      author='Franco Pellegrini',
      author_email='frapell@ravvit.net',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pywapi',
          'Plone>=4.1',
          'plone.app.registry',
          'collective.z3cform.widgets',
      ],
      extras_require={
        'test': ['plone.app.testing']
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
