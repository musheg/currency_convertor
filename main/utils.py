from datetime import datetime, timedelta
from collections import defaultdict

from pandasdmx import Request


class CurrencyConvertor(object):
    # TODO: save ECB data into DB to avoid frequently requests
    # TODO: use some cache engine (like Memcached or Redis) for performance
    def __init__(self, from_currencies: list, to_currencies: list, start_period: datetime.date, end_period: datetime.date):
        self.from_currencies = from_currencies
        self.to_currencies = to_currencies
        self.start_period = start_period
        self.end_period = end_period

    @staticmethod
    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def __get_rates_in_euro(self):
        ecb = Request('ECB')
        start_period = self.start_period.strftime('%Y-%m-%d')
        end_period = self.end_period.strftime('%Y-%m-%d')
        all_currencies = self.to_currencies + self.from_currencies

        data_response = ecb.data(resource_id='EXR', key={'CURRENCY': all_currencies, "FREQ": "D"},
                                 params={'startPeriod': start_period, 'endPeriod': end_period})
        data = data_response.data

        euro_rates = defaultdict(dict)
        for val in data:
            for obs in val.obs:
                freq, from_currency, to_currency, ex_type, series_variation = obs.series_key.get_values()
                date = obs.dimension.get_values()[0]
                ex_rate = obs.value
                euro_rates[from_currency][date] = ex_rate
        return self.__normalize_data(euro_rates)

    def __normalize_data(self, euro_rates):
        """
        When no data is available for a specific day (for example, a holiday or a weekend), the
        day will include the last known values from previous days.
        """
        for single_date in self.date_range(self.start_period, self.end_period):
            for currency, rates in euro_rates.items():
                single_date_str = single_date.strftime('%Y-%m-%d')
                if not rates.get(single_date_str):
                    while True:
                        # TODO: here we can have potential infinite recursion, fix it
                        prev_day = single_date - timedelta(days=1)
                        prev_day_str = prev_day.strftime('%Y-%m-%d')
                        if rates.get(prev_day_str):
                            euro_rates[currency][single_date_str] = rates.get(prev_day_str)
                            break
        return euro_rates

    def convert_currencies(self):
        euro_rates = self.__get_rates_in_euro()
        response = []
        for from_currency in self.from_currencies:
            for to_currency in self.to_currencies:
                for date, ex_rate in euro_rates[from_currency].items():
                    converted_rate = float(euro_rates[to_currency][date])/float(euro_rates[from_currency][date])
                    response.append({
                        "from_currency": from_currency,
                        "to_currency": to_currency,
                        "date": date,
                        "converted_rate": converted_rate,
                    })
        return response
