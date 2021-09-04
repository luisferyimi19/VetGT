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
from django.conf import settings
from companies.models import Company
from utils.models import validate_profile_picture_size
import os
import hashlib
from django.core.validators import MaxValueValidator, MinValueValidator


def _picture_path_service(instance, filename):
    new_filename = hashlib.sha224(
        str(instance.name).encode('utf-8')).hexdigest()
    return os.path.join(
        'uploads',
        'services',
        new_filename[0:2],
        new_filename[2:4],
        '%s' % filename)


class Picture(models.Model):
    name = models.CharField(_(u"Nombre de imagenes"),
                            max_length=80, blank=True, null=True)
    picture1 = ImageField(_(u"Imagen 1"), max_length=500, null=True, blank=True,
                          upload_to=_picture_path_service, validators=[validate_profile_picture_size])
    picture2 = ImageField(_(u"Imagen 2"), max_length=500, null=True, blank=True,
                          upload_to=_picture_path_service, validators=[validate_profile_picture_size])
    picture3 = ImageField(_(u"Imagen 3"), max_length=500, null=True, blank=True,
                          upload_to=_picture_path_service, validators=[validate_profile_picture_size])
    picture4 = ImageField(_(u"Imagen 4"), max_length=500, null=True, blank=True,
                          upload_to=_picture_path_service, validators=[validate_profile_picture_size])

    class Meta:
        verbose_name = _(u"Foto")
        verbose_name_plural = _(u"Fotos")

    def __str__(self):
        return _(u"{}".format(self.name))

    @property
    def title(self):
        return self.name


class Service(models.Model):
    service_name = models.CharField(
        _(u"Nombre"), max_length=80, blank=True, null=True)

    creation_date = models.DateTimeField(
        _(u"Fecha de creación"), auto_now_add=True, null=True, blank=True)

    is_active = models.BooleanField(_(u"¿Esta activo?"), default=False)

    company = models.ForeignKey(
        Company,
        verbose_name=_(u"Empresa"),
        null=True,
        on_delete=models.CASCADE,
        blank=True)

    class Meta:
        verbose_name = _(u"Servicio")
        verbose_name_plural = _(u"Servicios")

    def __str__(self):
        return _(u"Servicio de {}".format(self.service_name))

    @property
    def name(self):
        return self.service_name


def validate_interval(value):
    if value < 0.0:
        raise ValidationError(_(u"El valor no puede ser negativo"))


class ServiceDescription(models.Model):
    description = models.TextField(_(u"Descripción"), null=True, blank=True)

    pictures = models.ForeignKey(
        Picture,
        verbose_name=_(u"Imagenes"),
        null=True,
        on_delete=models.SET_NULL,
        blank=True)

    service = models.ForeignKey(
        Service,
        verbose_name=_(u"Servicio"),
        null=True,
        on_delete=models.CASCADE,
        blank=True)

    price = models.FloatField(_(u"Precio"), validators=[validate_interval])

    promotion_percentage = models.FloatField(
        _(u"Porcentaje de promoción"), validators=[validate_interval])

    has_offer = models.BooleanField(_(u"¿Tiene oferta?"), default=False)

    url = models.CharField(
        _(u"Sitio Web"), max_length=100, blank=True, default="")

    class Meta:
        verbose_name = _(u"Descripción de servicio")
        verbose_name_plural = _(u"Descripción de servicios")

    def __str__(self):
        return _(u"Descripción de {}".format(self.service.name))

    @property
    def name(self):
        return self.name
