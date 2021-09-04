# -*- coding: utf-8 -*-
""" . """
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
from dateutil.relativedelta import relativedelta
from sorl.thumbnail import ImageField, get_thumbnail
from django.urls import reverse
from datetime import datetime
from utils.models import Address, validate_profile_picture_size, Phone
import hashlib
import cairo
import random
from django.core.files import File
import os

CIRCLE_GRADIENTS_USER = [
    ((217.0 / 255.0, 43 / 255.0, 228 / 255.0),
     (207 / 255.0, 6.0 / 255.0, 223 / 255.0)),
    ((56.0 / 255.0, 199.0 / 255.0, 243.0 / 255.0),
     (34 / 255.0, 188.0 / 255.0, 242.0 / 255.0)),
    ((255.0 / 255.0, 140.0 / 255.0, 2.0 / 255.0),
     (255 / 255.0, 119.0 / 255.0, 0.0 / 255.0)),
    ((254.0 / 255.0, 98.0 / 255.0, 100.0 / 255.0),
     (254 / 255.0, 78.0 / 255.0, 82.0 / 255.0)),
    ((0.0 / 255.0, 200.0 / 255.0, 110.0 / 255.0),
     (3 / 255.0, 189.0 / 255.0, 93.0 / 255.0)),
    ((254.0 / 255.0, 54.0 / 255.0, 130.0 / 255.0),
     (250 / 255.0, 34.0 / 255.0, 107.0 / 255.0)),
    ((166.0 / 255.0, 227.0 / 255.0, 0.0 / 255.0),
     (152 / 255.0, 221.0 / 255.0, 0.0 / 255.0)),
    ((4.0 / 255.0, 171.0 / 255.0, 164.0 / 255.0),
     (0 / 255.0, 156.0 / 255.0, 147.0 / 255.0)),
    ((255.0 / 255.0, 205.0 / 255.0, 2.0 / 255.0),
     (255 / 255.0, 197.0 / 255.0, 2.0 / 255.0)),
    ((127.0 / 255.0, 116.0 / 255.0, 238.0 / 255.0),
     (111 / 255.0, 94.0 / 255.0, 234.0 / 255.0)),
]

CIRCLE_GRADIENTS_VETERINARIAN = [
    ((0.0 / 255.0, 100 / 255.0, 94 / 255.0),
     (1 / 255.0, 85.0 / 255.0, 80 / 255.0)),
]


def _picture_path(instance, filename):
    new_filename = hashlib.sha224(
        str(instance.email).encode('utf-8')).hexdigest()
    return os.path.join(
        'static'
        'uploads',
        'users',
        new_filename[0:2],
        new_filename[2:4],
        '%s' % filename)


class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            first_name,
            last_name,
            password=None):
        """ . """
        if not email:
            raise ValueError(_("Los usuario deben tener un correo"))

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            first_name,
            last_name,
            password=None):

        if not email:
            raise ValueError(_("Los usuario deben tener un correo"))
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    GENDERS = (
        ('', _(u"Género")),
        ('undefined', _(u"Sin definir")),
        ('male', _(u"Masculino")),
        ('female', _(u"Femenino"))
    )

    def _picture_url(instance, filename):
        extension = filename.split('.')[-1]
        new_filename = hashlib.sha224('{}'.format(
            instance.email).encode('utf-8')).hexdigest()
        return '/'.join([
            'uploads',
            'users',
            new_filename[0:2],
            new_filename[2:4],
            '%s.%s' % (new_filename, extension)])

    address = models.ForeignKey(
        Address, blank=True, null=True, on_delete=models.SET_NULL)

    birthdate = models.DateField(
        _(u"Fecha de nacimiento"),
        null=True,
        blank=True
    )

    gender = models.CharField(
        _(u"Género"),
        max_length=25,
        choices=GENDERS,
        null=True,
        blank=True)

    phone = models.ForeignKey(
        Phone,
        verbose_name=_(u"Teléfono"),
        null=True,
        on_delete=models.SET_NULL,
        blank=True)

    profile_picture = ImageField(
        _(u"Imagen de perfil"),
        max_length=500,
        null=True,
        blank=True,
        upload_to=_picture_path,
        validators=[validate_profile_picture_size])

    cui = models.CharField(
        _(u"CUI"),
        max_length=100,
        null=True,
        blank=True)

    has_limited_access = models.BooleanField(
        _(u"Accesso limitado"),
        default=False)

    dont_expire_session = models.BooleanField(
        _(u"Expirar sesión"),
        default=True)

    first_name = models.CharField(_(u"Nombres"), max_length=255)

    last_name = models.CharField(_(u"Apellidos"), max_length=255)

    email = models.EmailField(
        _(u'Correo electrónico'),
        unique=True,
        blank=False,
        error_messages={
            'unique': _(u"Un usuario con este correo ya existe"), 'required': _(u"Este campo es requerido "),
        })
    username = models.CharField(
        _(u"Nombre de usuario"), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(_(u'¿Esta activo?'), default=True)

    is_admin = models.BooleanField(_(u'¿Es un Administrador?'), default=False)

    is_staff = models.BooleanField(_(u'¿Es un Staff?'), default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        # The special thing of this function is the temporal update, to check
        # the "picture_has_changed" event in ``self.save()``.
        self.__original_profile_picture = self.profile_picture

    def __str__(self):
        return u"{}, {}".format(self.last_name, self.first_name)

    class Meta:
        verbose_name = _(u"Usuario")
        verbose_name_plural = _(u"Usuarios")

    @property
    def pretty_name(self):
        """ Returns the pretty name string of the user. """
        if self.first_name:
            return self.first_name
        else:
            return self.email

    @property
    def formal_name(self):
        """ Returns the formal name string of the user. """
        if self.first_name:
            return '%s %s' % (self.first_name, self.last_name)
        else:
            return self.email

    @property
    def short_formal_name(self):
        first_name = self.first_name.strip()
        last_name = self.last_name.strip()
        names = first_name.split(" ")
        last_names = last_name.split(" ")

        if len(names) > 0 and len(last_names) > 0:
            return u"%s %s" % (names[0], last_names[0])

        else:
            if len(names) > 0:
                return self.first_name
            elif len(last_names) > 0:
                return self.last_name

        return u"%s" % self.email

    @property
    def first_last_name_and_full_names(self):

        first_name = self.first_name.strip()
        last_name = self.last_name.strip()
        names = first_name.split(" ")
        last_names = last_name.split(" ")

        if len(names) > 0 and len(last_names) > 1:
            return u"%s %s, %s" % (last_names[0], last_names[1], names[0])

        if len(names) > 1 and len(last_names) > 0:
            return u"%s %s" % (last_names[0], names[0])

        else:
            if len(names) > 0:
                return self.first_name
            elif len(last_names) > 0:
                return self.last_name

        return u"%s" % self.email

    @property
    def reverse_short_formal_name(self):

        first_name = self.first_name.strip()
        last_name = self.last_name.strip()
        names = first_name.split()
        last_names = last_name.split()

        if names and last_names:
            ln = last_names[0]

            if len(last_names) > 2:
                ln = "%s %s" % (last_names[0], last_names[1])
            return "%s, %s" % (ln, names[0])

        return self.first_name

    @property
    def first_first_name(self):

        first_name = self.first_name.strip()
        name = first_name
        if ' ' in name:
            for a in name.split(' '):
                if a != '':
                    return a
        else:
            return name

    @property
    def age(self):
        now = datetime.now()
        difference = relativedelta(now, self.birthdate)
        return difference.years

    def get_profile_picture_thumbnail(self, size):
        return get_thumbnail(
            self.profile_picture,
            '%sx%s' % (size, size),
            crop='center').url

    def generate_avatar(self):

        imagesize = (200, 200)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *imagesize)
        cr2 = cairo.Context(surface)

        lg3 = cairo.LinearGradient(0, 0, 200, 200)
        if hasattr(self, 'veterinarianprofile'):
            color = random.choice(CIRCLE_GRADIENTS_VETERINARIAN)
        else:
            color = random.choice(CIRCLE_GRADIENTS_USER)

        lg3.add_color_stop_rgb(0.49, color[0][0], color[0][1], color[0][2])
        lg3.add_color_stop_rgb(0.50, color[1][0], color[1][1], color[1][2])

        cr2.rectangle(0, 0, 200, 200)
        cr2.set_source(lg3)
        cr2.fill()
        # TEXT
        cr2.select_font_face(
            "Montserrat", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr2.set_font_size(60)
        cr2.set_source_rgb(255, 255, 255)
        cr2.fill_preserve()

        initials = self.initials
        (x, y, width, height, dx, dy) = cr2.text_extents(initials)
        cr2.move_to(((imagesize[0] - width) / 2.0) - 4 + (6 if initials[0] == 'J' else 0),
                    ((imagesize[1] + height) / 2.0) - 1 - (12 if 'J' in initials else 0))
        cr2.show_text(initials)

        if self.pk:
            file_name = "avatar" + str(self.pk) + ".png"
        else:
            file_name = "avatar.png"

        surface.write_to_png(file_name)
        f = open(file_name, 'rb')
        self.profile_picture = File(f)
        self.save()

        f.close()
        os.remove(file_name)


class PasswordRetrievalEvent(models.Model):
    user = models.ForeignKey('User', verbose_name=_(
        u"Usuario"), on_delete=models.CASCADE)
    token = models.CharField(_(u"Token"), max_length=20)
    is_consumed = models.BooleanField(_(u"¿Está consumido?"), default=False)
    created = models.DateTimeField(_(u"Creado"), auto_now_add=True)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = _(u"Evento de recuperación de password")
        verbose_name_plural = _(u"Eventos de recuperación de password")
        db_table = 'users_password_retrieval_event'
