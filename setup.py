from setuptools import setup, find_packages
import sys, os

version = '0.2.0'

README = os.path.join(os.path.dirname(__file__),
                      'README.rst')

setup(name='nagifo',
      version=version,
      description="Nagios notifications through notifo",
      long_description=open(README).read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='notifo flask nagios nagifo icinga',
      author='Dominic LoBue',
      author_email='dominic.lobue@gmail.com',
      url='https://github.com/dlobue/nagifo',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      data_files=[
          ('config', ['nagifo.wsgi', 'nagifo.conf']),
      ],
      scripts = ['bin/nagifo'],
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'notifo',
          'flask',
          'python-nagext',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
