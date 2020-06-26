import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def get_start(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_all_reports = types.InlineKeyboardButton(text='Все отчеты', callback_data='all_reports')
    item_other_reports = types.InlineKeyboardButton(text='Список отчетов', callback_data='other_reports')

    markup_inline.add(item_all_reports, item_other_reports)
    bot.send_message(message.chat.id, 'Отчеты',
                     reply_markup=markup_inline
                     )


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'all_reports':
        bot.send_message(call.message.chat.id, 'Тут скоро появится общий отчет')
    elif call.data == 'other_reports':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_leads = types.KeyboardButton('Отчет по лидам')
        item_sales = types.KeyboardButton('Отчет по продажам')
        item_deals = types.KeyboardButton('Отчет по сделкам')

        markup_reply.add(item_leads, item_sales, item_deals)
        bot.send_message(call.message.chat.id, 'Выбирете из списка',
                         reply_markup=markup_reply)


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Отчет по лидам':
        bot.send_message(message.chat.id, 'Тут скоро появится отчет по лидам')
    elif message.text == 'Отчет по продажам':
        bot.send_message(message.chat.id, 'Тут скоро появится отчет по продажам')
    elif message.text == 'Отчет по сделкам':
        bot.send_message(message.chat.id, 'Тут скоро появится отчет по сделкам')


bot.polling(none_stop=True)
