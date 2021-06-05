from telebot import types
import telebot
import random
import conf
import csv


"""
✅ на команды /start и /help пользователю присылается описание бота
✅ реализованы две клавиатуры в ответ на вопросы про характер и про интенсивность эмоции
✅ результаты опроса записываются в results.csv
* на основании данных из results.csv пользователю присылается фидбек: 
  как его ответы соотносятся с ответами остальных 
  (можно привести статистику по количеству опрошенных, по возрастному распределению, 
  по представленным городам)
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
                     "Если хотите начать, вызовите команду /sticker 🌟.\n\n"
                     "Если вдруг вам не понравился стикер и вы хотите другой, "
                     "просто напиши /sticker еще раз!\n\n"
                     "Вы сможете ознакомиться с результатами исследования (в формате документа csv), "
                     "как только пройдете его. Напишите /results")


user_data = {}


@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    sticker = random.choice(sticker_ids)
    user_data['sticker_id'] = sticker
    user_data['user_id'] = message.chat.id
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
    # Сохраняем полученную информацию в csv
    with open('results.csv', 'a') as csvf1:
        writer = csv.writer(csvf1, delimiter=' ')
        writer.writerow(user_data.values())
    # Показываем статистику
    respondents = set()
    cities = {}
    with open('results.csv', 'r') as csvf2:
        headers = csvf2.readline()
        for answer in csv.reader(csvf2, delimiter=' '):
            respondents.add(answer[1])
            if answer[8] not in cities:
                cities[answer[8].lower()] = 1
            else:
                cities[answer[8].lower()] += 1

    bot.send_message(message.chat.id, f'Вы – {len(respondents)}-й респондент! Круто!')
    bot.send_message(message.chat.id, f'А еще вы {cities[user_data["city"]]}-й респондент из города {user_data["city"]}!')

    # Хочет ли информант продолжить
    answer = message.text.strip()
    if answer == 'Да':
        bot.send_message(message.chat.id, 'Продолжим!')
        send_sticker(message)
    else:
        bot.send_message(message.chat.id, 'Спасибо! До скорого ☺️')


@bot.message_handler(commands=['results'])
def send_doc(message):
    with open('results.csv', 'r') as f:
        bot.send_document(message.chat.id, f)


if __name__ == '__main__':
    bot.polling(none_stop=True)
