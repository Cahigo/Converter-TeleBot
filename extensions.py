import requests
import json

from config import currency


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(base, quote, amount):
        if base == quote:
            raise APIException(f"Перевести {base} в себя же нельзя")

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {base}")
        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {quote}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Значение 'количество' должно быть числом")

        if amount <= 0:
            raise APIException("Значение 'количество' должно быть больше нуля")

        r = requests.get(f"https://api.coingate.com/v2/rates/merchant/{base_ticker}/{quote_ticker}")
        return json.loads(r.content)
