from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=25)
    subject = models.CharField(max_length=25)
    message = models.CharField(max_length=254)


class ContactUsCreate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    reply_to = models.EmailField(max_length=25)
    subject = models.CharField(max_length=128)
    body = models.CharField(max_length=1024)
    raw_content = models.TextField()


class Rate(models.Model):
    type = models.EmailField(max_length=5)  # noqa: A003
    source = models.CharField(max_length=64)
    created = models.DateTimeField()
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    contact_namber = models.CharField(max_length=15)
