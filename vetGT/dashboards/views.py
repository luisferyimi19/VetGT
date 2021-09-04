from django.http import HttpResponse
from django.template import loader
from companies.models import Company
from services.models import Service, ServiceDescription, Picture
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from django.shortcuts import render, redirect


def index(request):
    template = loader.get_template('web/index.html')
    companies = Company.objects.all()
    count = 0
    company_count = 0
    companies_dict = {}
    companies_dict[company_count] = []
    for company in companies:
        if company.has_marketing:
            count += 1
            if count < 4:
                companies_dict[company_count].append(company)
            else:
                company_count += 1
                companies_dict[company_count] = []
                count = 1
                companies_dict[company_count].append(company)

    services = Service.objects.filter(is_active=True)
    count = 0
    service_count = 0
    services_dict = {}
    services_dict[service_count] = []
    for service in services:
        if service.is_active:
            service_description = ServiceDescription.objects.get(
                service=service)
            if service_description.has_offer and service_description.promotion_percentage:
                price = service_description.price * \
                    (service_description.promotion_percentage / 100)
                service.current_price = service_description.price - price

                service.price = service_description.price
                service.has_offer = service_description.has_offer
                service.description = service_description.description
                service.url = service_description.url
                service.pictures = service_description.pictures
                count += 1
                if count < 4:
                    services_dict[service_count].append(service)
                else:
                    service_count += 1
                    services_dict[service_count] = []
                    count = 1
                    services_dict[service_count].append(service)

    context = {
        'companies': companies_dict,
        'services': services_dict
    }
    return HttpResponse(template.render(context, request))


def brands(request):
    template = loader.get_template('web/brands.html')
    companies = Company.objects.all()
    count = 0
    company_count = 0
    companies_dict = {}
    for company in companies:
        if company.has_marketing:
            company_count += 1
            companies_dict[company_count] = []
            companies_dict[company_count].append(company)
    context = {
        'companies': companies_dict
    }
    return HttpResponse(template.render(context, request))


def services(request):
    template = loader.get_template('web/services.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def my_pet(request):
    template = loader.get_template('web/my_pet.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def contact(request):
    template = loader.get_template('web/contact.html')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com',
                          ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("dashboards:homepage")
    form = ContactForm()
    return render(request, template, {'form': form})
