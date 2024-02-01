#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
import io

VERSION = '1.0.1' 
DESCRIPTION = 'hfinder'

pwd = path.abspath(path.dirname(__file__))
with io.open(path.join(pwd, "README.md"), encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name="hfinder", 
    version=VERSION,
    author="Sébastien Copin",
    author_email="cosad3s@outlook.com",
    license="GPL-3.0 License",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["beautifulsoup4","requests","argparse","webdriver-manager"],
    url="https://github.com/cosad3s/hfinder",
    keywords=['hostnames', 'cidr', 'asn', 'network', 'discovery', 'osint', 'bugbounty'],
    entry_points={
        "console_scripts": [
            "hfinder = hfinder.__main__:main"
        ]
    },
    include_package_data = True,
    classifiers= [
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Security",
        "Programming Language :: Python :: 3"
    ]
)