from currency import model_choices as mch

from django.db import models
from django.templatetags.static import static


def upload_logo(instance, filename: str) -> str:
    return f'{instance.name}/logo/{filename}'


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    code_name = models.PositiveSmallIntegerField(choices=mch.SourceCodeName.choices, unique=True)
    name = models.CharField(max_length=64, unique=True)
    contact_namber = models.CharField(max_length=15)
    logo_bank = models.FileField(upload_to=upload_logo, default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def logo_bank_url(self):
        if self.logo_bank:
            return self.logo_bank.url

        return static('img/no_logo')


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
    type = models.CharField(max_length=5, choices=mch.RateType.choices)  # noqa: A003
    base_type = models.CharField(max_length=10, choices=mch.RateType.choices, default=mch.RateType.UAH)
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE)
