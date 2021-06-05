import os
import telebot
import pandas as pd
import numpy as np
import conf


"""
Какую семантику и эмоциональную окраску пользователи приписывают стикерам/гифам? 
Бот посылает пользователю стикеры/гифы по одному (выберите 5-10 ваших любимых) 
и просит ответить на вопросы 
    "Если бы ваш друг прислал бы вам сообщение вместо стикера/гифа, каким бы оно могло быть?", 
    "В ответ на какое сообщение вы бы могли отправить этот стикер/гиф?", 
    "С какой эмоцией у вас ассоциируется этот стикер/гиф?" (варианты  на клавиатуре), 
    "Насколько интенсивна эта эмоция?" (от 0 до 5, на клавиатуре), 
    "Сколько вам лет?", 
    "Какой ваш родной язык?", 
    "В каком городе вы живете?". 
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
    'CAACAgIAAxkBAAECYgABYLqmg2PVULz2pyLxD7EWhE-7S0wAAi0FAAIjBQ0AAbcJ8hMMlOv8HwQ', 
    'CAACAgIAAxkBAAECYf5guqaBUte5XlrW-yTkEvPUk2gTjQAClgUAAiMFDQAB093MX0k8ti0fBA', 
    'CAACAgIAAxkBAAECYfxguqZ6UuavTBXx0383_Y_XYNLD-AACsgADfyesDob98AUq_JgcHwQ', 
    'CAACAgIAAxkBAAECYflguqZ0jFdNnK3I2FfyXSrPBXOgZwACtAADfyesDlHseKGO5zatHwQ', 
    'CAACAgIAAxkBAAECYfhguqZyonYQylS-0_WMaijUYBAxUwACswADfyesDoye8IP1WFJxHwQ', 
    'CAACAgIAAxkBAAECYfZguqZrA_bmRSu09w9udkkdVOmiFQACkAADfyesDrBBtxz9WHj7HwQ', 
    'CAACAgIAAxkBAAECYfRguqZmZ1xOirfN_mj8toe2s3VJfgACVwADfyesDoWEEgIh3JQaHwQ', 
    'CAACAgIAAxkBAAECYfJguqZdbIdunjHYzsG52zVk4fYVhAACUAADSIQLAAFAyTdDSZlo6B8E', 
    'CAACAgIAAxkBAAECYfBguqZV6rxKcaclYW7mZNBmGj5jtwACBQEAAjyKVxrKuyM_Svr6jh8E', 
    'CAACAgIAAxkBAAECYe5guqZCB-EZkFIjv7ZfUlcxN6mz8QACBQADenb4EXXLZTUI7DV4HwQ', 
    'CAACAgUAAxkBAAECYexguqY6MjbMLtpNeBGcbDeo_iRzHwACUQcAAszG4gI45CvG55BOXh8E', 
    'CAACAgIAAxkBAAECYeZguqYsZTjR3y_xQxEQiB8KtV6ICAACGAADenb4EXFNJy-jEA1jHwQ', 
    'CAACAgIAAxkBAAECYeRguqYkgdDNy0VJgRcmA9K86NQ67AAC7QADPIpXGh5vcLokkxR7HwQ'
]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Hi there! This bot helps linguists to carry out a "
                     "sticker sentiment analysis :) You are only required "
                     "to answer simple questions!")


# bot.send_sticker(chat_id=update.message.chat_id, sticker='CAADAgADOQADfyesDlKEqOOd72VKAg')

    
if __name__ == '__main__':
    bot.polling(none_stop=True)
