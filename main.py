import telebot
from config import TOKEN, currency
from extensions import APIException, Converter
from math import fabs

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = f"""{message.chat.username}, Вас приветствует Бот-конвертер!

Чтобы начать работу со мной, введите команду в формате:
<ваша_валюта> <во_что_переводим> <сколько_переводим>
    
Пример ввода:    рубль доллар 100
(перевод ста рублей в доллары)

Количество переводимой валюты можно выразить как целым числом, так и десятичной дробью. Для разделения целой и дробной части нужно использовать точку.

Доступные команды:
/values — посмотреть все доступные валюты
/start или /help — вызвать это сообщение ещё раз"""

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"

    for key in currency.keys():
        text = '\n'.join((text, key))

    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        parameters = message.text.split(' ')

        if len(parameters) != 3:
            raise APIException("Команда введена неправильно.")

        base, quote, amount = parameters
        result = Converter.get_price(base, quote, amount)

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка на стороне пользователя.\n{e}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду.\n{e}")

    else:
        text = f"Цена {fabs(float(amount))} {base} в {quote} — {fabs(result)}"
        bot.reply_to(message, text)


@bot.message_handler(content_types=['photo', 'audio', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def error(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Я умею распознавать только текст.")


bot.polling(none_stop=True)
