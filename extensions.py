import requests
import json
from config import currency


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException("Не могу конвертировать валюту саму в себя.")

        try:
            base in currency.keys()
        except KeyError:
            raise APIException(f"Неизвестная валюта: {base}")

        try:
            quote in currency.keys()
        except KeyError:
            raise APIException(f"Неизвестная валюта: {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Введено неверное число для валюты.")

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={currency[base]}&symbols={currency[quote]}")

        result = json.loads(r.content)

        return round(result['rates'][currency[quote]] * amount, 2)
