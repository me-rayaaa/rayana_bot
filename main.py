import telebot
import requests
import random
from telebot import types

bot = telebot.TeleBot("тттт")


@bot.message_handler(commands=['help'])
def display_help(message):
    help_text = """
/start - начало
/help - сообщение со справкой 
/info - информация о боте

/exchange_rate - курс валюты 
/weather <город> - погода в выбранном городе
/joke - анекдот 
/cube - бросить игральную кость
/ip - <ip адрес>- страна, область и город по ip 
/guess_number - игра «Угадай число»
/compliment - коплимент для вас!)
"""
    bot.reply_to(message, help_text)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я Раяна! 👩🏻 Используй команду /help для получения справки.")
    photo = open('image.jpg', 'rb')  # Открываем фотографию в бинарном режиме
    bot.send_photo(message.chat.id, photo)  # Отправляем фото по идентификатору чата
    photo.close()  # Закрываем файл


@bot.message_handler(commands=['info'])
def info(message):
    first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\nХочешь расскажу немного о себе?"
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    markup.add(button_yes)
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def response(function_call):
    if function_call.message:
        if function_call.data == "yes":
            second_mess = "Я универсальный бот-помощник Раяна. 🥰 Познакомиться с создателем ты можешь, перейдя по ссылке!"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Перейти на сайт VK", url="https://vk.com/me.rayaaa"))
            bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            bot.answer_callback_query(function_call.id)


@bot.message_handler(commands=['exchange_rate'])
def exchange_rate(message):
    resp = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = resp.json()
    usd_rate = data['Valute']['USD']['Value']
    eur_rate = data['Valute']['EUR']['Value']
    exchange_rate_text = f'''
    Курс валют: 
USD {usd_rate} руб. 💵
EUR {eur_rate} руб. 💶
    '''
    bot.reply_to(message, exchange_rate_text)
    bot.reply_to(message, '💵')
    bot.reply_to(message, '💶')


@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        city = message.text.split(' ', 1)[1]  # Получаем город из сообщения пользователя
        api_key = "3f9cc2afa48f311d34d0780ab04f8d12"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url)
        data = resp.json()
        temperature = data['main']['temp']
        weather_text = f"Погода в {city}: температура: {temperature}°C"
        bot.reply_to(message, weather_text)
        bot.reply_to(message, "⛅")
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите город после команды /weather.")
        bot.reply_to(message, "⛅⛅⛅")


@bot.message_handler(commands=['joke'])
def joke(message):
    resp = requests.get("https://api.chucknorris.io/jokes/random")
    data = resp.json()
    joke_text = data['value']
    bot.reply_to(message, joke_text)


@bot.message_handler(commands=['cube'])
def cube(message):
    dice_value = random.randint(1, 6)
    emoji_dice = "🎲"  # Emoji для отображения значений на кубике
    bot.reply_to(message, f"На кубике выпало число {dice_value}.")
    bot.reply_to(message, f"{emoji_dice}")


@bot.message_handler(commands=['ip'])
def get_location_by_ip(message):
    try:
        ip_address = message.text.split(' ', 1)[1]  # Получаем IP-адрес из сообщения пользователя
        resp = requests.get(f"http://ipinfo.io/{ip_address}/json")
        data = resp.json()
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        location_text = f"Местоположение для IP-адреса {ip_address}: {city}, {region}, {country}"
        bot.reply_to(message, location_text)
        bot.reply_to(message, '💡💡💡')
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите IP-адрес после команды /ip. ")
        bot.reply_to(message, "💡💡💡")


# Обработчик команды для начала игры
@bot.message_handler(commands=['guess_number'])
def start_game(message):
    global secret_number  # Генерируем новое случайное число для каждой новой игры
    secret_number = random.randint(1, 100)
    bot.reply_to(message, "Давай поиграем в 'Угадай число'! Я загадал число от 1 до 100. Попробуй угадать.")


# Обработчик сообщений для угадывания числа
@bot.message_handler(func=lambda message: message.text.isdigit())
def guess_number(message):
    guess = int(message.text)
    if guess < secret_number:
        bot.reply_to(message, "Загаданное число больше.")
    elif guess > secret_number:
        bot.reply_to(message, "Загаданное число меньше.")
    else:
        bot.reply_to(message,
                     f"Поздравляю, ты угадал число {secret_number}! Хочешь сыграть еще раз? 🫢 Используй команду /guess_number.")


compliments = [
    "Вы прекрасно справляетесь!",
    "Ваш труд неоценим!",
    "Вы делаете мир ярче!",
    "Ваш вклад важен!",
    "Продолжайте в том же духе!",
    "Ваш оптимизм невероятен!",
    "Вас слушать - одно удовольствие!",
    "Очень круто! Продолжайте в том же духе!",
    "Ваше усердие вдохновляет!",
    "Ваша работа - искусство!",
]


# Обработчик команды для отправки комплимента о команде
@bot.message_handler(commands=['compliment'])
def send_compliment(message):
    compliment = random.choice(compliments)
    bot.reply_to(message, compliment)


phrases = [
    "Классное изображение!",
    "Замечательная фотография!",
    "Прекрасное изображение!",
    "Впечатляющая картинка!",
    "Спасибо за фото!"
]


# Обработчик отправленных изображений
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    random_phrase = random.choice(phrases)
    bot.reply_to(message, random_phrase)


# Обработчик команды для сохранения данных в файл
@bot.message_handler(commands=['save_data'])
def save_data(message):
    user_id = message.from_user.id
    user_data = "Some data to save"

    # Записываем данные в текстовый файл
    with open(f"{user_id}_data.txt", "w") as file:
        file.write(user_data)

    bot.reply_to(message, "Данные успешно сохранены.")


# Обработчик команды для чтения данных из файла
@bot.message_handler(commands=['read_data'])
def read_data(message):
    user_id = message.from_user.id

    # Читаем данные из текстового файла
    try:
        with open(f"{user_id}_data.txt", "r") as file:
            data = file.read()
            bot.reply_to(message, f"Ваши данные: {data}")
    except FileNotFoundError:
        bot.reply_to(message, "Данные не найдены.")


bot.polling()
