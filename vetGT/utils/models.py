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

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
import os
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
import hashlib
from django.template.defaultfilters import filesizeformat


def validate_profile_picture_size(value):
    """
        Validates the profile picture maximum size
    """
    if value.file.size > int(settings.PROFILE_PICTURE_MAX_UPLOAD_SIZE):
        raise ValidationError(
            _(u"Por favor mantén el tamaño del archivo abajo de %(max_size)s. Actualmente pesa %(current)s") % (
                {
                    'max_size': filesizeformat(settings.PROFILE_PICTURE_MAX_UPLOAD_SIZE),
                    'current': filesizeformat(value.file.size)
                }
            )
        )


class Address(models.Model):
    address1 = models.CharField(max_length=500, blank=True, null=True)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    address3 = models.CharField(max_length=500, blank=True, null=True)
    address4 = models.CharField(max_length=500, blank=True, null=True)
    address5 = models.TextField(blank=True, null=True)
    address6 = models.TextField(blank=True, null=True)

    def __str__(self):
        return u"{}, {}, {}, {}, {}".format(
            self.address1,
            self.address2,
            self.address4,
            self.address5,
            self.address3
        )


class SingletonModel(models.Model):
    """
    Abstracts the behaviour of a single instance model class.

    :members:
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Saves the SingletonModel

        If there is no preivous register, create one. Else, delete the only
        register available and create a new one.

        :rtype: None.
        """

        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        If there is no preivous register, create one. Else, return the one that
        is first registered.

        :rtype: None.
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class InheritanceCastModel(models.Model):
    """
    An abstract base class that provides a ``real_type`` FK to ContentType.

    For use in trees of inherited models, to be able to downcast parent
    instances to their child types.

    :members:
    """

    real_type = models.ForeignKey(
        ContentType, editable=False, on_delete=models.CASCADE)
    """
    ForeignKey to the content type used to instantiate this model register.
    """

    def save(self, *args, **kwargs):
        """
        Saves self's ContentType reference before actually saving the object.

        :rtype: None.
        """
        if not self.id:
            self.real_type = self._get_real_type()
        super(InheritanceCastModel, self).save(*args, **kwargs)

    def _get_real_type(self):
        """
        Catches the real_type of self and gets it's reference in ContentType.

        :param self: reference to the current register.
        :rtype: ContentType object.
        """
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        """
        Queries for the object of the referenced type with self's primary key.

        :rtype: Model.
        """
        return self.real_type.get_object_for_this_type(pk=self.pk)

    class Meta:
        abstract = True


class Country(models.Model):
    """
    Simple country representation, mostly for addresses or phones.

    :members:
    """

    name = models.CharField(_(u"Nombre"), max_length=50)
    """Name for the country."""

    short_name = models.CharField(_(u"Nombre corto"), max_length=2)
    """Human identifier for the country."""

    phone_prefix = models.CharField(_(u"Prefijo de teléfono"), max_length=3)
    """Country phone prefix attached for mobile interfaces."""

    @classmethod
    def get_default(cls):
        return Country.objects.get(name=settings.INSTANCE_COUNTRY)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"País")
        verbose_name_plural = _(u"Países")


class PhoneLabel(models.Model):
    """
    Simple phone type identifier (eg. Home, Work, Mobile).

    :members:
    """

    name = models.CharField(_(u"Nombre"), max_length=50)
    """Phone book search index."""

    @classmethod
    def get_default(cls):
        return PhoneLabel.objects.get(name=settings.INSTANCE_DEFAULT_PHONE_LABEL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Etiqueta de teléfono")
        verbose_name_plural = _(u"Etiquetas de teléfono")


class Phone(models.Model):
    """
    Simple phone representation. A phone always has a label and a country

    :members:
    """

    country = models.ForeignKey(
        Country,
        verbose_name=_(u"País"),
        null=True,
        on_delete=models.SET_NULL)
    """ForeignKey to know where the phone comes from."""

    number = models.CharField(
        _(u"Teléfono"), max_length=100, blank=True, default="")
    """The phone's number."""

    label = models.ForeignKey(
        PhoneLabel,
        verbose_name=_(u"Etiqueta"),
        null=True,
        on_delete=models.SET_NULL)
    """ForeignKey to identify the phone usage context."""

    @property
    def first_value(self):
        splitted = self.number.split(',')

        if len(splitted) > 0:
            return splitted[0]

        return self.number

    def __str__(self):
        # TODO v1.0
        return ""


class CustomHttpResponseRedirect(HttpResponseRedirect):
    allowed_schemes = ['http', 'https', 'ftp', 'android-app']
