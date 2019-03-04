"""
allcities - Python library to access all the cities of the world with a population of at least 1000 inhabitants.
"""

#!/usr/bin/env python3
# coding: utf-8

__version__ = '1.0.3'
__author__ = 'Jonathan Chun'
__author_email__ = 'git@jonathanchun.com'

import time

from .core import all_cities as cities
from .core import download_update, init, last_update

init()
