# -*- coding: utf-8 -*-
"""
Description
"""
__version__ = '0.1.0'
__author__ = 'Luis Dávila <luisdaviladeleon@gmail.com>'
__date__ = '19 August 2021'
__copyright__ = 'Copyright (c) 2021 Luis Dávila'
__license__ = 'THE LICENSE'
__status__ = 'development'
__docformat__ = 'reStructuredText'

from django.db import models
from django.utils.translation import ugettext as _
from sorl.thumbnail import ImageField
from django.core.exceptions import ValidationError
import hashlib
import os
from django.conf import settings
from django.template.defaultfilters import filesizeformat
