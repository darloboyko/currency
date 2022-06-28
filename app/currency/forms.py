from currency.models import Rate, Source

from django import forms


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('source_url', 'logo_bank', 'name', 'contact_namber')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('type', 'source', 'buy', 'sale')
