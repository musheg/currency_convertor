from django import forms


class CurrencyConvertForm(forms.Form):
    CURRENCY_CHOICES = [
        ('EUR', 'EUR'),
        ('USD', 'USD'),
        ('JPY', 'JPY'),
        ('BGN', 'BGN'),
        ('CZK', 'CZK'),
        ('DKK', 'DKK'),
        ('GBP', 'GBP'),
        ('HUF', 'HUF'),
        ('PLN', 'PLN'),
        ('RON', 'RON'),
        ('SEK', 'SEK'),
        ('CHF', 'CHF'),
        ('ISK', 'ISK'),
        ('NOK', 'NOK'),
        ('HRK', 'HRK'),
        ('RUB', 'RUB'),
        ('TRY', 'TRY'),
        ('AUD', 'AUD'),
        ('BRL', 'BRL'),
        ('CAD', 'CAD'),
        ('CNY', 'CNY'),
        ('HKD', 'HKD'),
        ('IDR', 'IDR'),
        ('ILS', 'ILS'),
        ('INR', 'INR'),
        ('KRW', 'KRW'),
        ('MXN', 'MXN'),
        ('MYR', 'MYR'),
        ('NZD', 'NZD'),
        ('PHP', 'PHP'),
        ('SGD', 'SGD'),
        ('THB', 'THB'),
        ('ZAR', 'ZAR'),
    ]

    # TODO: form validation!
    from_currencies = forms.MultipleChoiceField(choices=CURRENCY_CHOICES)
    to_currencies = forms.MultipleChoiceField(choices=CURRENCY_CHOICES)
    from_date = forms.DateField()
    to_date = forms.DateField()