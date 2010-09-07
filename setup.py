from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='nagifo',
      version=version,
      description="Nagios notifications through notifo",
      long_description="""\
Nagios notifications through notifo, plus a small webapp to acknowledge the alert""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='notifo flask nagios',
      author='Dominic LoBue',
      author_email='dominic.lobue@gmail.com',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )