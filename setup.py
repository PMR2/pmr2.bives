from setuptools import setup, find_packages
import os

version = '0.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='pmr2.bives',
      version=version,
      description="PMR2 BiVeS integration",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Tommy Yu',
      author_email='tommy.yu@auckland.ac.nz',
      url='https://github.com/PMR2/pmr2.bives',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['pmr2'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'pmr2.cytoscape',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
