from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('brands/', views.brands, name='brands'),
    path('services/', views.services, name='services'),
    path('mypet/', views.my_pet, name='my_pet'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
]
