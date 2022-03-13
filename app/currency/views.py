from currency.models import ContactUs

from django.http import HttpResponse


def contact_list(request):
    contacts = []
    for contact in ContactUs.objects.all():
        contacts.append([contact.id, contact.email_from, contact.subject, contact.message])
    return HttpResponse(str(contacts))
