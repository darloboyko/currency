import re
from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from currency import model_choices as mch

import requests


def round_decimal(value: str) -> Decimal:
    places = Decimal(10) ** -2
    return Decimal(value).quantize(places)


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
        'BTC': mch.RateType.BTC,
        'UAH': mch.RateType.UAH,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.PRIVATBANK)[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['ccy'])
        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate["base_ccy"])

        sale = round_decimal(rate["sale"])
        buy = round_decimal(rate["buy"])

        last_rate = Rate.objects\
            .filter(source=source, type=currency_type)\
            .order_by("created").last()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_monobank():
    from currency.models import Rate, Source
    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        978: mch.RateType.USD,
        840: mch.RateType.EUR,
        980: mch.RateType.UAH,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.MONOBANK)[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['currencyCodeA'])
        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['currencyCodeB'])

        sale = round_decimal(rate['rateSell'])
        buy = round_decimal(rate['rateBuy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type) \
            .order_by("created").last()

        if (last_rate is None or
                last_rate.sale != rate['rateSell'] or
                last_rate.buy != rate['rateBuy']):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_vkurse():
    from currency.models import Rate, Source
    url = "http://vkurse.dp.ua/course.json"
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'Dollar': mch.RateType.USD,
        'Euro': mch.RateType.EUR,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.VKURSE)[0]

    for key_rate, val_rate in rates.items():
        currency_type = available_currencies.get(key_rate)
        if not currency_type:
            continue

        base_currency_type = mch.RateType.UAH

        sale = round_decimal(val_rate["sale"])
        buy = round_decimal(val_rate["buy"])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type) \
            .order_by("created").last()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_oschadbank():
    from currency.models import Rate, Source

    url = "https://www.oschadbank.ua/currency-rate"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    response.raise_for_status()
    rates = soup.find('tbody', class_='heading-block-currency-rate__table-body')
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.OSCHADBANK)[0]

    headers_rates = []
    for all_rate in rates.find_all('tr', class_='heading-block-currency-rate__table-row'):
        headers_rates.append(all_rate)

        for rate in headers_rates:
            currency_type = available_currencies.get(rate.find_all('td', class_='heading-block-currency-rate__table-col')[1].get_text())
            if not currency_type:
                continue

            sale = round_decimal(rate.find_all('td', class_='heading-block-currency-rate__table-col')[3].get_text())
            buy = round_decimal(rate.find_all('td', class_='heading-block-currency-rate__table-col')[4].get_text())

            base_currency_type = mch.RateType.UAH

            last_rate = Rate.objects \
                .filter(source=source, type=currency_type) \
                .order_by("created").last()

            if (last_rate is None or  # does not exist in table
                    last_rate.sale != sale or
                    last_rate.buy != buy):
                Rate.objects.create(
                    type=currency_type,
                    base_type=base_currency_type,
                    sale=sale,
                    buy=buy,
                    source=source,
                )


@shared_task
def parse_ukrsibbank():
    from currency.models import Rate, Source

    url = "https://my.ukrsibbank.com/ua/personal/operations/currency_exchange/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    response.raise_for_status()
    rates = soup.find('tbody')
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.UKRSIBBANK)[0]

    headers_rates = []
    for all_rate in rates.find_all('tr'):
        headers_rates.append(all_rate)

        for rate in headers_rates:
            i = rate.find_all("td")
            for _ in i:
                currency_type = available_currencies.get(i[0].get_text().split(',')[0])
                if not currency_type:
                    continue

                sale = round_decimal(re.sub('[^0-9, .]', '', i[1].get_text()))
                buy = round_decimal(re.sub('[^0-9, .]', '', i[2].get_text()))

                base_currency_type = mch.RateType.UAH

                last_rate = Rate.objects \
                    .filter(source=source, type=currency_type) \
                    .order_by("created").last()

                if (last_rate is None or  # does not exist in table
                        last_rate.sale != sale or
                        last_rate.buy != buy):
                    Rate.objects.create(
                        type=currency_type,
                        base_type=base_currency_type,
                        sale=sale,
                        buy=buy,
                        source=source,
                    )


@shared_task
def parse_raiffeisen():
    from currency.models import Rate, Source

    url = "https://finance.ua/ua/banks/raiffeisen-bank-aval/currency"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    response.raise_for_status()
    rates = soup.find("div", class_="sc-7eg87i-1 fPmITI")
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.RAIFFEISEN)[0]

    headers_rates = []

    for all_rate in rates.find_all('tbody', class_="sc-tu3zio-4 lgYGob"):
        headers_rates.append(all_rate)

        for rate in headers_rates:
            i = rate.find_all("tr")
            for n in i:
                currency_type = available_currencies.get(n.get_text()[0:3])
                if not currency_type:
                    continue

                sale = round_decimal(n.get_text()[3:8].replace(',', '.'))
                buy = round_decimal(n.get_text()[14:19].replace(',', '.'))

                base_currency_type = mch.RateType.UAH

                last_rate = Rate.objects \
                    .filter(source=source, type=currency_type) \
                    .order_by("created").last()

                if (last_rate is None or  # does not exist in table
                        last_rate.sale != sale or
                        last_rate.buy != buy):
                    Rate.objects.create(
                        type=currency_type,
                        base_type=base_currency_type,
                        sale=sale,
                        buy=buy,
                        source=source,
                    )
