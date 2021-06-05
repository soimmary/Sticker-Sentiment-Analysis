import os
import telebot
from telebot import types
import pandas as pd
import numpy as np
import conf

"""
- send sticker
- answer questions
- wanna another one? y/n


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
* реализованы две клавиатуры в ответ на вопросы про характер и про интенсивность эмоции
* результаты опроса записываются в results.csv
* на основании данных из results.csv пользователю присылается фидбек: как его ответы соотносятся с ответами остальных 
  (можно привести статистику по количеству опрошенных, по возрастному распределению, по представленным городам, 
  по характеру приписываемой эмоции, по интенсивности эмоции)
* реализована возможность перейти к следующему стикеру/гифу или завершить опрос
"""

bot = telebot.TeleBot(conf.TOKEN)
sticker_ids = [
    'CAACAgIAAxkBAAECYkNgu2PoW9bCYv7JgLlPr1MKmt76KAAC7QADPIpXGh5vcLokkxR7HwQ',
    'CAACAgIAAxkBAAECYkVgu2P0_2aKGjsqru0qgP2fEJ9mZQACGAADenb4EXFNJy-jEA1jHwQ',
    'CAACAgIAAxkBAAECYkdgu2QF_NrKsn6PUq7kQAqgbg5Q7gACLQUAAiMFDQABtwnyEwyU6_wfBA',
    'CAACAgUAAxkBAAECYktgu2Qa6PnKc5-JusUR3_ilo0eHNQACxQYAAszG4gK3wUYfyR3TSR8E',
    'CAACAgIAAxkBAAECYk9gu2RIvNxErcaHrXLrav9euuuA_QACpwADfyesDlW4WzNWUWRgHwQ'
]

# Создаем словарь
user_data = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()

    # добавляем на нее две кнопки
    button1 = types.InlineKeyboardButton(text="Да", callback_data="button_yes")
    button2 = types.InlineKeyboardButton(text="Нет", callback_data="button_no")
    keyboard.add(button1)
    keyboard.add(button2)

    bot.send_message(message.chat.id,
                     "Привет! Этот бот помогает лингвистам проводить сентимент-анализ "
                     "с использованием стикеров в Телеграме! Предлагаем вам ответить "
                     "на несколько простых вопросов :) Начнем?", reply_markup=keyboard)


# функция запустится, когда пользователь нажмет на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "button_yes":
            send_sticker(call.message.chat.id)
        if call.data == "button_no":
            bot.send_message(call.message.chat.id, "Хорошо. Тогда, до сокрого!")

            
def send_sticker(message):
    for sticker in sticker_ids:
        bot.send_sticker(message.chat.id, sticker)


if __name__ == '__main__':
    bot.polling(none_stop=True)
