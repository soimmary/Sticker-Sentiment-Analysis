from telebot import types
import telebot
import random
import conf


"""
Бот посылает пользователю стикеры/гифы по одному (выберите 5-10 ваших любимых) 
и просит ответить на вопросы 
    1. "Если бы ваш друг прислал бы вам сообщение вместо стикера/гифа, каким бы оно могло быть?", 
    2. "В ответ на какое сообщение вы бы могли отправить этот стикер/гиф?", 
    3. "С какой эмоцией у вас ассоциируется этот стикер/гиф?" (варианты  на клавиатуре), 
    4. "Насколько интенсивна эта эмоция?" (от 0 до 5, на клавиатуре), 
    5. "Сколько вам лет?", 
    6. "Какой ваш родной язык?", 
    7. "В каком городе вы живете?". 
Ответы пользователя записываются в results.csv. 
В конце серии вопросов по стикеру/гифу пользователю присылается благодарность 
    ("Вы первый, кто прокомментировал этот стикер/гиф" 
    или Большинство опрошенных ассоциирует этот стикер/гиф с интенсивной злостью,
    или любая другая статистика на основе собранных данных) 
и возможность перейти к следующему стикеру/гифу или завершить опрос


✅ на команды /start и /help пользователю присылается описание бота
✅ реализованы две клавиатуры в ответ на вопросы про характер и про интенсивность эмоции
* результаты опроса записываются в results.csv
* на основании данных из results.csv пользователю присылается фидбек: 
  как его ответы соотносятся с ответами остальных 
  (можно привести статистику по количеству опрошенных, по возрастному распределению, 
  по представленным городам, по характеру приписываемой эмоции, по интенсивности эмоции)
✅ реализована возможность перейти к следующему стикеру/гифу или завершить опрос
"""

bot = telebot.TeleBot(conf.TOKEN)
sticker_ids = [
    'CAACAgIAAxkBAAECYkNgu2PoW9bCYv7JgLlPr1MKmt76KAAC7QADPIpXGh5vcLokkxR7HwQ',
    'CAACAgIAAxkBAAECYkVgu2P0_2aKGjsqru0qgP2fEJ9mZQACGAADenb4EXFNJy-jEA1jHwQ',
    'CAACAgIAAxkBAAECYkdgu2QF_NrKsn6PUq7kQAqgbg5Q7gACLQUAAiMFDQABtwnyEwyU6_wfBA',
    'CAACAgUAAxkBAAECYktgu2Qa6PnKc5-JusUR3_ilo0eHNQACxQYAAszG4gK3wUYfyR3TSR8E',
    'CAACAgIAAxkBAAECYk9gu2RIvNxErcaHrXLrav9euuuA_QACpwADfyesDlW4WzNWUWRgHwQ',
    'CAACAgIAAxkBAAECYs1gu5HgGAJgByQ1PoDRao9OSrSKEQACrgADfyesDmEN9hyD4C20HwQ',
    'CAACAgIAAxkBAAECYtBgu5Hus3ZAT25zOKGp7Kx81uK3GQACpgADfyesDpUUIUQjXhW_HwQ',
    'CAACAgQAAxkBAAECYtJgu5H7uShSBk6LBk81GETORp9MxAACIwADX8YBGblN6Er12GDkHwQ',
    'CAACAgIAAxkBAAECYtRgu5ILZJUVxTKG_gad38qSpZy8AQACegUAAiMFDQABbpLHbsuBRvUfBA',
    'CAACAgIAAxkBAAECYtZgu5Ic9l8y6Zq1SIqlj1Fd67guwgACMgUAAiMFDQABe6yTTsfJ4MYfBA'
]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Этот бот помогает лингвистам проводить сентимент-анализ "
                     "с использованием стикеров в Телеграме! Предлагаем вам ответить "
                     "на несколько простых вопросов :)\n\n"
                     "Если хочешь начать, вызови команду /sticker 🌟.\n\n"
                     "Если вдруг тебе не понравился стикер, просто напиши /sticker еще раз!")

user_data = {}
# отправляем стикер
@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    user_data['user_id'] = message.chat.id
    sticker = random.choice(sticker_ids)
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id,
                     '1. Если бы ваш друг прислал вам сообщение вместо этого стикера, '
                     'каким бы оно могло быть?')
    bot.register_next_step_handler(message, q1)


def q1(message):
    user_data['q1'] = message.text
    bot.send_message(message.chat.id,
                     '2. В ответ на какое сообщение вы бы могли отправить этот стикер?')
    bot.register_next_step_handler(message, q2)


def q2(message):
    user_data['q2'] = message.text
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('/😄', '/🥰', '/🤨', '/🥺', '/😡', '/😎', '/😢', 'другое')
    bot.send_message(message.chat.id,
                     '3. С какой эмоцией у вас ассоциируется этот стикер?',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, q3)


def q3(message):
    user_data['q3'] = message.text
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('0', '1', '2', '3', '4', '5')
    bot.send_message(message.chat.id,
                     '4. Насколько интенсивна эта эмоция?',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, q4)


def q4(message):
    user_data['q4'] = message.text
    bot.send_message(message.chat.id,
                     'Сколько вам лет?')
    bot.register_next_step_handler(message, age)


def age(message):
    user_data['age'] = message.text
    bot.send_message(message.chat.id,
                     'Какой ваш родной язык?')
    bot.register_next_step_handler(message, lang)


def lang(message):
    user_data['lang'] = message.text
    bot.send_message(message.chat.id,
                     'В каком городе вы живете?')
    bot.register_next_step_handler(message, city)


def city(message):
    user_data['city'] = message.text
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Да', 'Нет')
    bot.send_message(message.chat.id, 'Хотите продолжить?', reply_markup=keyboard)
    bot.register_next_step_handler(message, if_continue)


def if_continue(message):
    answer = message.text.strip()
    if answer == 'Да':
        bot.send_message(message.chat.id, 'Круто!')
        send_sticker(message)
    else:
        bot.send_message(message.chat.id, user_data)
        bot.send_message(message.chat.id, 'Спасибо! До скорого ☺️')


if __name__ == '__main__':
    bot.polling(none_stop=True)
