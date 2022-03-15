from currency.models import ContactUs

from django.shortcuts import render


def contact_list(request):
    contacts = ContactUs.objects.all()
    return render(request, 'contact_list.html', context={'contacts': contacts})


def index(request):
    return render(request, 'index.html')
