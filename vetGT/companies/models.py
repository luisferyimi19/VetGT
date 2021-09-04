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
import os
from django.conf import settings
from utils.models import Phone, validate_profile_picture_size, Address
import hashlib


def _picture_path_company(instance, filename):
    new_filename = hashlib.sha224(
        str(instance.company_name).encode('utf-8')).hexdigest()
    return os.path.join(
        'uploads',
        'companies',
        '%s' % filename)


class Company(models.Model):

    company_name = models.CharField(_(u"Nombre"), max_length=80, unique=True, blank=False, error_messages={
        'unique': _(u"Un compañia con este nombre ya existe"), 'required': _(u"Este campo es requerido")})
    address = models.ForeignKey(Address, verbose_name=_(
        u"Dirección"), blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.ForeignKey(
        Phone,
        verbose_name=_(u"Teléfono"),
        null=True,
        on_delete=models.SET_NULL,
        blank=True)

    email = models.EmailField(_(u'Correo electrónico'), unique=True, blank=False, error_messages={
                              'unique': _(u"Un usuario con este correo ya existe"), 'required': _(u"Este campo es requerido")})
    facebook = models.CharField(
        _(u"Facebook"), max_length=100, blank=True, default="")

    instagram = models.CharField(
        _(u"Instagram"), max_length=100, blank=True, default="")

    twitter = models.CharField(
        _(u"Twitter"), max_length=100, blank=True, default="")

    web_page = models.CharField(
        _(u"Sitio Web"), max_length=100, blank=True, default="")

    logo = ImageField(
        _(u"Logo"),
        max_length=500,
        null=True,
        blank=True,
        upload_to=_picture_path_company,
        validators=[validate_profile_picture_size])

    description = models.TextField(
        _(u"Descripción de compañia"), null=True, blank=True)

    has_marketing = models.BooleanField(
        _(u"¿Tiene marketing?"),
        default=False)

    class Meta:
        verbose_name = _(u"Compañia")
        verbose_name_plural = _(u"Compañias")

    def __str__(self):
        return _(u"Compañia {}".format((self.company_name)))

    @property
    def name(self):
        return self.company_name
