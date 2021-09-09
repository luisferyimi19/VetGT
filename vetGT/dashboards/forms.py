from django import forms
from django.core.mail import message
from django.forms.widgets import Textarea

# Create your forms here.


class ContactForm(forms.Form):
    full_name_contact = forms.CharField(max_length=50, required=True,label='Nombre completo')
    email_address_contact = forms.EmailField(max_length=150, required=True, label='Correo')
    message_contact = forms.CharField(widget=forms.Textarea, required=True, max_length=2000, label='Contenido')
    subject_contact = forms.CharField(max_length=50, required=True, label='Asunto')