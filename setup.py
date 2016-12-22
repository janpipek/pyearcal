#!/usr/bin/env python
from setuptools import setup, find_packages
import itertools

options = dict(
    name='pyearcal',
    version='0.3.0',
    packages=find_packages(),
    license='MIT',
    description='Year calendar creation in Python',
    long_description=open('README.md').read(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/pyearcal',
    install_requires = ['reportlab', 'pillow', 'python-dateutil'],
    extras_require = {
        'flickr' : ['beautifulsoup4', 'requests']
    }
    # entry_points = {
    #     'console_scripts' : [
    #         'pyercal = <TODO>'
    #     ]
    # }
)

extras = options['extras_require']
extras['full'] = list(set(itertools.chain.from_iterable(extras.values())))
setup(**options)