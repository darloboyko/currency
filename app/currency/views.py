from currency.forms import SourceForm
from currency.models import ContactUs, ContactUsCreate, Rate, Source

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class ContactUsList(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contact_list.html'


class ContactUsCreate(CreateView):
    model = ContactUsCreate
    template_name = "contactus_create.html"
    success_url = reverse_lazy('index')
    fields = ('name', 'reply_to', 'subject', 'body')

    def _send_email(self):
        subject = 'User ContactUs'
        body = f'''
            Request From: {self.object.name}
            Email to reply: {self.object.reply_to}
            Subject: {self.object.subject}

            Body: {self.object.body}
        '''
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_email()
        return redirect


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'rate_list.html'


class SourceList(ListView):
    queryset = Source.objects.all().order_by('-id')
    template_name = 'source_list.html'


class SourceDetail(DetailView):
    model = Source
    template_name = 'source_detail.html'


class SourceCreate(CreateView):
    model = Source
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceUpdate(UpdateView):
    model = Source
    template_name = 'source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceDelete(DeleteView):
    model = Source
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')
