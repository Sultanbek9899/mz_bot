import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    doc = open('Политика_в_отношении_обработки_персональных_данных_3.pdf', 'rb')
    # keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Принимаю", callback_data='accept')
    item2 = types.InlineKeyboardButton("Отклонить", callback_data='cancel')

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, данный бот предназначен для передачи информаии ".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


bot.polling(none_stop=True)