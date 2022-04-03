from currency.models import ContactUs
from currency.models import Rate

from django.shortcuts import render


def contact_list(request):
    contacts = ContactUs.objects.all()
    return render(request, 'contact_list.html', context={'contacts': contacts})


def rate_list(request):
    rates = Rate.objects.all()
    return render(request, 'rate_list.html', context={'rates': rates})


def index(request):
    return render(request, 'index.html')
