import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Данный бот конвертирует валюту. Отправьте сообщение в '
                                      'формате: <имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо '
                                      'узнать цену первой валюты> <количество первой валюты>. Для того чтобы узнать '
                                      'список валют - введите команду /values.'.format(message.from_user))


@bot.message_handler(commands=['values'])
def values_print(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def conversion(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Слишком много параметров")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
