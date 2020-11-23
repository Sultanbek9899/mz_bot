import telebot
import config
from telebot import types
from sql import SQLighter
from datetime import datetime
bot = telebot.TeleBot(config.TOKEN)
db = SQLighter('db.db')


def text_format(user_id, username):
    info_list = db.get_user_info(user_id)
    print(info_list)
    id = info_list[0] #в базе данных
    searcher_name = info_list[2]
    pin = info_list[3]
    relations = info_list[4]
    phone_number = info_list[5]
    patient_name = info_list[6]
    birth_date = info_list[7]
    hospitalization_date = info_list[8]
    hospitalization_place = info_list[9]
    now = datetime.now()
    text = f"""
        Время отправки: {now}
        Пользоваталь телеграмм: @ {username}
        №: {id} 
        Имя ищущего: {searcher_name},
        ПИН: {pin},
        Кем приходится больному: {relations},
        Номер телефона: {phone_number},
        Имя больного: {patient_name},
        Дата рождения больного: {birth_date},
        Дата госпитилизации: {hospitalization_date},
        Место госпитилизации(отделение/палата):{hospitalization_place},
    """
    return text


@bot.message_handler(commands=['start'])
def welcome(message):
    doc = open('Политика_в_отношении_обработки_персональных_данных_3.pdf', 'rb')
    # keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Принимаю", callback_data='accept')
    item2 = types.InlineKeyboardButton("Отклонить", callback_data='cancel')
    markup.add(item1, item2)
    text = """Добро пожаловать, данный бот предназначен для передачи информаии о состоянии пациентов 
     в стационарах для их близкиx. Если вы хотите получить информацию о состоянии ваших родных , пожалуйста , 
     прочитайте "Соглашение в отношении обработки персональных данных" ,если вы согласы нажмите на кнопки "Принимаю".
    """
    if not db.table_exist():
        db.create_table()
    bot.send_document(message.chat.id, doc)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['reset'])
def delete_all_info(message):
    pass


@bot.message_handler(content_types=['text'])
def get_full_name(message): #получаем фамилию
    full_name = message.text
    if not db.user_exists(message.from_user.id):
        db.add_new_user(message.from_user.id, 'full_name', message.text)
    else:
        db.update_info(message.from_user.id, 'full_name', full_name)
    bot.send_message(message.chat.id, 'Напишите ваш ПИН')
    bot.register_next_step_handler(message, get_pin)


def get_pin(message):
    while len(message.text) != 14:
        bot.send_message(message, 'Пожалуйста , введите , корректный ПИН')
    pin = message.text  # проверяем, что возраст введен корректно
    db.update_info(message.from_user.id, 'pin', pin)

    bot.send_message(message.from_user.id, 'Кем вы являетесь больному?')
    bot.register_next_step_handler(message, get_family_relationship)


def get_family_relationship(message):
    relationship = message.text
    db.update_info(message.from_user.id, 'relationship', relationship)
    bot.send_message(message.chat.id, 'Пожалуйста, напишите , ваш номер телефона по которому с вами могу связаться наш оператор')
    bot.register_next_step_handler(message, get_phone_number)


def get_phone_number(message):
    phone=message.text
    db.update_info(message.from_user.id, 'phone_number', phone)
    bot.send_message(message.from_user.id, 'Теперь, пожалуйста , введите Ф.И.О. больного')
    bot.register_next_step_handler(message, get_patient_name)


def get_patient_name(message):
    patient_name = message.text
    db.update_info(message.from_user.id, 'patient_name', patient_name)
    bot.send_message(message.chat.id, 'Пожалуйста , введите год рождение больного')
    bot.register_next_step_handler(message, get_patient_year_birth)


def get_patient_year_birth(message):
    patient_date = message.text
    db.update_info(message.from_user.id, 'date_of_birth', patient_date)
    bot.send_message(message.chat.id, 'Пожалуйста , введите дату госпитилизации больного(Пример: 16.09.2020): ')
    bot.register_next_step_handler(message, get_date_hospitalization)


def get_date_hospitalization(message):
    date = message.text
    db.update_info(message.from_user.id, 'hospitalization_date', date)
    bot.send_message(message.chat.id, 'Пожалуйста, введите место госпитилизации больного(по возмодности напишите отделение или палату)')
    bot.register_next_step_handler(message, get_hospital)


def get_hospital(message):
    hospital = message.text
    db.update_info(message.from_user.id, 'hospitalization_place', hospital)
    bot.send_message(message.chat.id,'Спасибо! Пожалуйста, ожидайте , наш оператор свяжется с вами для предоставления запращиваемой вами информации')

    bot.send_message(1217299182,
                     text_format(message.from_user.id, message.from_user.username))
    bot.send_message(message.from_user.id, text_format(message.from_user.id, message.from_user.username))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'accept':
                bot.send_message(call.message.chat.id, 'Пожалуйста, введите ваше Ф.И.О.')
            elif call.data == 'cancel':
                bot.send_message(call.message.chat.id, 'Вы отклонили соглашение')
            # remove inline buttons
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, , reply_markup=None)
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)