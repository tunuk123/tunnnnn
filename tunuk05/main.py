import telebot
import datetime

TOKEN = '6848201317:AAFqQdWkQdE3wfN6okkbsX4mqyV9BrZJs7o'

bot = telebot.AsyncTeleBot( token = TOKEN )


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Я бот который устанавливает таймер.',
                     reply_markup=get_keyboard())


@bot.callback_query_handlers(func=lambda x: x.data == 'set timer')
def pre_set_timer(query):
    message = query.message
    bot.send_message(message.chat.id,
                     'Введите время для установки таймера.\n'
                     'Пример ввода: \n'
                     '1.20 сек\n'
                     '2.2 мин\n'
                     '3.10 час')
    bot.register_next_step_handler(message,set_time)


def set_time(message):
    times= {
        'сек':0,
        'мин':0,
        'час':0
    }

    quantity,type_time=message.text.split()

    if type_time not in times.keys():
        bot.send_message(message.chat.id,
                         'Вы ввели неправильный тип времени.')
        return

    if not quantity.isdigit():
        bot.send_message(message.chat.id,
                         'Вы ввели не число')

    times[type_time]=int(quantity)

    cur_date=datetime.datetime.now()


    timedelta=datetime.timedelta(days=0,seconds=times['сек'],
                                 minutes=times['мин'],hours=times['час'])

    cur_date+=timedelta

    pre_set_text(message,cur_date)


def pre_set_text(message,cur_date):
    bot.send_message(message.chat.id,
                     'Введите текст , который придет после '
                          'истечения таймера.')
    bot.register_next_step_handler(message, set_text, cur_date)


def set_text(message,cur_date):
    users[message.chat.id]=(cur_date,message.text)
    bot.send_message(message.chat.id,
                     'Спасибо!Через заданное время вам придет уведомление.')


def get_keyboard():
    keyboard=telebot.types.InlineKeyboardMarkup()
    button=telebot.types.InlineKeyboardButton('Установить таймер', callback_data='set timer')
    keyboard.add(button)
    return keyboard


if __name__ == '__main__':
    users= {}
    while True:
        try:
            bot.polling()
        except:
            print('Что-то сломалось. Перезагрузка')

