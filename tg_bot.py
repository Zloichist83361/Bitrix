import telebot
import config
from telebot import types
from datetime import datetime
from bitrix_get_report import create_deal, create_all_sum_deal, create_lead
from decimal import Decimal

date_create = datetime.now().date()

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def get_start(message):
    markup_reply = types.ReplyKeyboardMarkup()
    item_lead_report = types.KeyboardButton(text='Отчет по лидам')
    item_deal_report = types.KeyboardButton(text='Отчет по сделкам')
    item_all_sum_report = types.KeyboardButton(text='Общая сумма продаж')

    markup_reply.add(item_lead_report, item_deal_report, item_all_sum_report)
    bot.send_message(message.chat.id, 'ОТЧЕТЫ',
                     reply_markup=markup_reply)




@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Отчет по лидам':
        bot.send_message(message.chat.id, f' Отчет по лидам за {date_create} : \n'
                                          f'{create_lead()}')
    elif message.text == 'Отчет по сделкам':
        bot.send_message(message.chat.id, f' Отчет по сделкам за {date_create} : \n'
                                          f'{create_deal()}')
    elif message.text == 'Общая сумма продаж':
        bot.send_message(message.chat.id, f' Общая сумма продаж за {date_create} : \n'
                                          f'{sum(Decimal(sum_sales) for sum_sales in create_all_sum_deal())} RUB')



if __name__ == '__main__':
    bot.infinity_polling()
