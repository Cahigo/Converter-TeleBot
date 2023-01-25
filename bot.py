import telebot

from config import currency, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):  # Приветствие
    text = "Этот бот выводит актуальную цену одной выбранной валюты на основе другой. " \
           "\nДля работы используйте следующий синтаксис: " \
           "\n<Какую валюту покупаем?> <Какой валютой платим?> <Сколько покупать?> " \
           "\nПример ввода: 'доллар рубль 100'" \
           "\nЧтобы узнать, какие валюты поддерживает бот, используйте комманду /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):  # Вывод валют
    text = "Доступные валюты: "
    for cur in currency.keys():
        text = "\n".join((text, cur))

    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(self: telebot.types.Message):  # Конвертация
    try:
        request = self.text.split(" ")
        if len(request) != 3:
            raise APIException("Неверный ввод! Пожалуйста, следуйте примеру. Помощь: /help")

        base, quote, amount = request
        result = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(self, f"Ошибка пользователя \n{e}")
    except Exception as e:
        bot.reply_to(self, f"Не удалось обработать команду \n{e}")
    else:
        total = result * int(amount)
        text = f"Цена {amount} {base} в {quote} = {total:0.2f}"
        bot.send_message(self.chat.id, text)


bot.polling()
