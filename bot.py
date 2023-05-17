# -*- coding: utf-8 -*-
from cover import draw_tag
import telebot
import sys

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
collected_data = {}

def request_text(message):
    bot.send_message(message.chat.id, '*** Введите текст ***')
    bot.register_next_step_handler(message, handle_text)

def request_link(message):
    bot.send_message(message.chat.id, '*** Введите ссылку ***')
    bot.register_next_step_handler(message, handle_link)

def request_tag(message):
    tag_keyboard = telebot.types.InlineKeyboardMarkup()
    tools_button = telebot.types.InlineKeyboardButton(text='tools', callback_data='tools')
    video_button = telebot.types.InlineKeyboardButton(text='video', callback_data='video')
    just_post_button = telebot.types.InlineKeyboardButton(text='just post', callback_data='just post')
    podcast_button = telebot.types.InlineKeyboardButton(text='podcast', callback_data='podcast')
    tag_keyboard.add(tools_button, video_button, just_post_button, podcast_button)
    bot.send_message(message.chat.id, '*** Выберите тег ***', reply_markup=tag_keyboard)


@bot.message_handler(commands=['start'])
def start_message(message):
    print(collected_data)
    collected_data.clear()
    request_text(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text
    collected_data["text"] = text
    request_link(message)

@bot.message_handler(content_types=['text'])
def handle_link(message):
    if message.text.startswith("http"):
        link = message.text
        collected_data["link"] = link
        request_tag(message)
    else:
        bot.send_message(message.chat.id, f'Нерабочая ссылка. Введите текст')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data in ['tools', 'video', 'just post', 'podcast']:
        collected_data["tag"] = call.data

        draw_tag(text=collected_data["text"], link=collected_data["link"], tag=collected_data["tag"])
        image = open('image_with_tag.jpg', 'rb')
        bot.send_photo(call.message.chat.id, image)
        bot.send_message(call.message.chat.id, 'Создать новую обложку')
        request_text(call.message)
    else:
        bot.send_message(call.message.chat.id, f'Неверный тег')
    print(collected_data)

bot.infinity_polling(timeout=10, long_polling_timeout = 5)






