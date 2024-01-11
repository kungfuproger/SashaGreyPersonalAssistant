import telebot # библиотека pyTelgramBotAPI
import webbrowser
import datetime as dt

from telebot import types
from weather_parse.weather_parse import weather

bot = telebot.TeleBot('6640731580:AAHeV5S5NWO2D_rm1TVPr2I8OlDWAtcuc5Y')


# Вспомогательные функции
def get_datetime():
    date_time = dt.datetime.now()
    time = date_time.time()
    date = dt.date.today()
    return date, time


# Обработка команд
@bot.message_handler(commands=['help'])
def help(message):
    response = (
        f'/start - Приветствие\n'
        f'/site - Сайт-портфолио (в разработке)\n'
        f'/ \n'
        f'/ \n'
        f'/ \n'
    )
    bot.send_message(message.chat.id, response)


task_list = '1. Улучшить любимого бота.'
@bot.message_handler(commands=['start'])
def start(message):
    response = (
        f'Привет, красавчик!\n'
        f'Сегодня {get_datetime()[0].strftime("%d-%m-%y")}\n'
        f'Вот список дел на сегодня:\n'
        f'{task_list}\n'
        f'Продуктиного дня!\n'
    )
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Прогноз погоды')
    btn2 = types.KeyboardButton('Фотография дня')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, response, reply_markup=markup)
    bot.register_next_step_handler(message, start_handler)


def start_handler(message):
    if message.text == 'Прогноз погоды':
        data = weather()
        bot.send_message(message.chat.id, f'Прогноз погоды на {get_datetime()[0].strftime("%d-%m-%y")}.\n{data[1]}')
    elif message.text == 'Фотография дня':
        bot.send_message(message.chat.id, 'Запускаю приложение Фотография дня.')


@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://google.com')

# Обработка текста
@bot.message_handler(chat_types=['text'])
def dialog(message):
    metatext = message.text.lower()
    if metatext == 'привет':
        response = 'Бла-бла-бла !'
    elif metatext == 'id':
        response = f'ID: {message.from_user.id}'
    elif metatext == 'а покажи сиськи':
        file = open('./SashaGrey/948177.jpg', 'rb')
        bot.send_photo(message.chat.id, file)
    elif metatext == 'видео с тобой':
        file = open('./SashaGrey/SGsolo4u.mp4', 'rb')
        bot.send_video(message.chat.id, file) # не работает
    else:
        response = 'хз'
    bot.reply_to(message, response)


# Обработка фото
class ImageCase():
    """Картинка с пояснением."""
    names = []
    
    def __init__(self, name, image, desc):
        if name in ImageCase.names:
            raise NameError('Назовите картинку по-другому.')
        self.name = name
        ImageCase.names.append(name)
        self.image = image
        self.desc = desc
    
    def get(self):
        return self.image, self.desc
    
    def get_name(self):
        return self.name


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Добавить описание', callback_data='desc')
    markup.row(btn1)
    bot.reply_to(message, 'Какое красивое фото', reply_markup=markup)


# Обработчик нажатия кнопки в markup'е
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'desc':
        bot.send_message(callback.message.chat.id, 'Реакцией на это должно быть добавление описание к картинке в базе.')


bot.polling(non_stop=True)
