from django.contrib import admin

from .models import Service, ServiceDescription, Picture

admin.site.register(Service)
admin.site.register(ServiceDescription)
admin.site.register(Picture)
