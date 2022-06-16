from datetime import datetime
from django.views.generic import TemplateView
from django.http import JsonResponse

from .utils import CurrencyConvertor
from .forms import CurrencyConvertForm


class CurrencyExchangeView(TemplateView):
    template_name = 'currency_exchange.html'
    form_class = CurrencyConvertForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        from_currencies = request.POST.getlist("from_currencies")
        to_currencies = request.POST.getlist("to_currencies")
        # TODO: validate date format coming from the form
        start_date = datetime.fromisoformat(request.POST.get("from_date"))
        end_date = datetime.fromisoformat(request.POST.get("to_date"))

        currency_convertor = CurrencyConvertor(from_currencies=from_currencies, to_currencies=to_currencies,
                                               start_period=start_date, end_period=end_date)
        resp = currency_convertor.convert_currencies()
        return JsonResponse({"response": resp}, status=200, json_dumps_params={"default": str})
