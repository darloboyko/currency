from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=15)
    subject = models.CharField(max_length=25)
    message = models.CharField(max_length=254)


class Rate(models.Model):
    type = models.EmailField(max_length=5)  # noqa: A003
    source = models.CharField(max_length=64)
    created = models.DateTimeField()
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)
