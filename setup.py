#!/usr/bin/env python
import itertools
from setuptools import setup, find_packages

options = dict(
    name="pyearcal",
    version="2021.0",
    packages=find_packages(),
    license="MIT",
    description="Year calendar creation in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jan Pipek",
    author_email="jan.pipek@gmail.com",
    url="https://github.com/janpipek/pyearcal",
    install_requires=["reportlab", "pillow", "python-dateutil", "click", "fonttools"],
    extras_require={"flickr": ["beautifulsoup4", "requests"]},
    python_requires=">=3.6",
    entry_points={"console_scripts": ["pyearcal=pyearcal.cli:run"]},
)

extras = options["extras_require"]
extras["full"] = list(set(itertools.chain.from_iterable(extras.values())))
setup(**options)
