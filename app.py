import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])#обработчик команд start/help
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате:\n(Нижний регистр, через пробел)\n<какую валюту переводим> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])#обработчик команды values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])#обработчик вводимого текста
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("Должно быть 3 параметра.")

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()