#!/usr/bin/env python
import itertools
from setuptools import setup, find_packages

options = dict(
    name='pyearcal',
    version='0.3.2',
    packages=find_packages(),
    license='MIT',
    description='Year calendar creation in Python',
    long_description=open('README.md').read(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/pyearcal',
    install_requires = ['reportlab', 'pillow', 'python-dateutil', 'click'],
    extras_require = {
        'flickr' : ['beautifulsoup4', 'requests']
    },
    entry_points = {
         'console_scripts' : [
             'pyearcal=pyearcal.cli:run'
         ]
    }
)

extras = options['extras_require']
extras['full'] = list(set(itertools.chain.from_iterable(extras.values())))
setup(**options)
