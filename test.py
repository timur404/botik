import datetime
import os
import random
import time

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('/Users/timur/Desktop/botik/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандом до 100")
    item2 = types.KeyboardButton("😉Как себя чувствуешь?")
    item3 = types.KeyboardButton("🎵Угадай мелодию")
    item4 = types.KeyboardButton("🕳Кинуть монетку")
    item5 = types.KeyboardButton("📝А какой план?")
    item6 = types.KeyboardButton("😔Мне нужна помощь")
    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, полезный бот, которого создал "
                     "Тимур. Он мой лучший друг:)".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=["voice"])
def content_text(message):
    bot.send_message(message.chat.id, '😄Давай не ленись, пиши пальчиками')


@bot.message_handler(content_types=['text'])
def take(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандом до 100':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😉Как себя чувствуешь?':
            markup = types.InlineKeyboardMarkup(row_width=5)
            item1 = types.InlineKeyboardButton("10", callback_data='10')
            item2 = types.InlineKeyboardButton("9", callback_data='9')
            item3 = types.InlineKeyboardButton("8", callback_data='8')
            item4 = types.InlineKeyboardButton("7", callback_data='7')
            item5 = types.InlineKeyboardButton("6", callback_data='6')
            item6 = types.InlineKeyboardButton("5", callback_data='5')
            item7 = types.InlineKeyboardButton("4", callback_data='4')
            item8 = types.InlineKeyboardButton("3", callback_data='3')
            item9 = types.InlineKeyboardButton("2", callback_data='2')
            item10 = types.InlineKeyboardButton("1", callback_data='1')

            markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)

        elif message.text == '🎵Угадай мелодию':
            for file in os.listdir('music/'):
                if file.split('.')[-1] == 'ogg':
                    f = open('music/' + file, 'rb')
                    msg = bot.send_voice(message.chat.id, f, None)
                time.sleep(3)

        elif message.text == '🕳Кинуть монетку':
            recoin = random.randint(0, 1)
            coin = "Орёл" if recoin else "Решка"
            bot.send_message(message.chat.id, str(coin))

        elif message.text == '📝А какой план?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Добавить таску",
                                               callback_data='done' if message.text != ' ' else 'Ты ничего не добавил')
            item2 = types.InlineKeyboardButton("Убрать последнее", callback_data='clear')

            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Давай изменим', reply_markup=markup)

        elif message.text == 'Добавить таску':
                task = 'Добавлено✅' if message.text != (' ' or '') else 'Ты ничего не добавил'
                bot.send_message(message.chat.id, task, reply_markup=markup)

        elif message.text == 'Убрать последнее':
                task = 'Убрать последнее'
                bot.send_message(message.chat.id, task, reply_markup=markup)
        elif message.text == '😔Мне нужна помощь':
            bot.send_message(message.chat.id, '🚨Уже выехала обьяснительная бригада')

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить, лучше используй клавиатуру 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == '10':
                bot.send_message(call.message.chat.id, 'Великолепно, ты счастлив')
            elif call.data == '9':
                bot.send_message(call.message.chat.id, 'Вот так его')
            elif call.data == '8':
                bot.send_message(call.message.chat.id, 'Давай ещё')
            elif call.data == '7':
                bot.send_message(call.message.chat.id, 'Шоу только начинается')
            elif call.data == '6':
                bot.send_message(call.message.chat.id, 'Нормально')
            elif call.data == '5':
                bot.send_message(call.message.chat.id, 'Могло быть и лучше')
            elif call.data == '4':
                bot.send_message(call.message.chat.id, 'Что-то не так, исправляй')
            elif call.data == '3':
                bot.send_message(call.message.chat.id, 'Блииин')
            elif call.data == '2':
                bot.send_message(call.message.chat.id, 'Давай без депрессий')
            elif call.data == '1':
                bot.send_message(call.message.chat.id, 'Наш корабль идёт ко дну')

            elif call.data == 'done':
                bot.send_message(call.message.chat.id, 'Добавлено✅')
            elif call.data == 'clear':
                bot.send_message(call.message.chat.id, 'Убрано✅')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" Принято) ",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Мне нравится с тобой общаться!")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
