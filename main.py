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
    text = """Добро пожаловать, данный бот предназначен для передачи информаии о состоянии пациентов 
     в стационарах для их близкиx. Если вы хотите получить информацию о состоянии ваших родных , пожалуйста , 
     прочитайте "Соглашение в отношении обработки персональных данных" ,если вы согласы нажмите на кнопки "Принимаю".
    """
    bot.send_document(message.chat.id, doc)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_full_name(message): #получаем фамилию
    global full_name
    full_name = message.text
    bot.send_message(message.from_user.id, 'Кем вы являетесь больному?')
    bot.register_next_step_handler(message, get_family_relationship)


def get_family_relationship(message):
    global relationship
    relationship = message.text
    bot.send_message(message.chat.id, 'Напишите ваш ПИН')
    bot.register_next_step_handler(message, get_pin)


def get_pin(message):
    global pin
    pin = message.text  # проверяем, что возраст введен корректно
    # bot.send_message(message, 'Пожалуйста , введите , корректный ПИН')
    bot.send_message(message.from_user.id, 'Теперь, пожалуйста , введите Ф.И.О. больного')
    bot.register_next_step_handler(message, get_patient_name)


def get_patient_name(message):
    global patient_name
    patient_name = message.text
    bot.send_message(message.chat.id, 'Пожалуйста , введите дату госпитилизации больного(Пример: 16.09.2020): ')
    bot.register_next_step_handler(message, get_date_hospitalization)


def get_date_hospitalization(message):
    global date
    date = message.text
    bot.send_message(message.chat.id, 'Пожалуйста, введите место госпитилизации больного(по возмодности напишите отделение или палату)')
    bot.register_next_step_handler(message, get_hospital)


def get_hospital(message):
    global hospital

    hospital = message.text
    bot.send_message(message.chat.id, 'Пожалуйста , введите год рождение больного')
    bot.register_next_step_handler(message, get_patient_year_birth)


def send_message_for_admin(text):
    bot.send_message(1217299182, text)


def get_patient_year_birth(message):
    global patient_date
    patient_date = message.text
    bot.send_message(message.chat.id, 'Спасибо! Пожалуйста, ожидайте , наш оператор свяжется с вами для предоставления запращиваемой вами информации')
    text=f"""
        Ф.И.О ищущего:{full_name},
        Кем он является больному: {relationship},
        ПИН:{pin},
        Имя пациента:{patient_name},
        Дата рождение:{patient_date},
        Дата госпитилизации: {date},
        Место госпитилизации: {hospital},
    """
    send_message_for_admin(text)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'accept':
                bot.send_message(call.message.chat.id, 'Пожалуйста, введите ваше Ф.И.О.')
            elif call.data == 'cancel':
                bot.send_message(call.message.chat.id, 'Вы отклонили соглашение')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, '', reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)