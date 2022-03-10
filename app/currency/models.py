from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=15)
    subject = models.CharField(max_length=25)
    message = models.CharField(max_length=254)
