from distutils import command
from extensions import APIException, APIRequester
import telebot
from telebot import types
import json

BOT_TOKEN = json.load(open('config.json'))["BOT_TOKEN"]

bot = telebot.TeleBot(token = BOT_TOKEN)

@bot.message_handler(commands =['start', 'help'])
def command_help(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    values = types.KeyboardButton("/values")
    convert = types.KeyboardButton("/convert")
    markup.add(values)
    markup.add(convert)
    bot.send_message(message.chat.id, 'Выберите опцию', reply_markup=markup)

@bot.message_handler(commands =['values'])
def command_values(message):
    reply_message = """Доступные валюты:
    USD	United States Dollar	United States
    EUR	Euro	European Union
    RUB	Russian Ruble	Russia
    BYN	Belarusian Ruble	Belarus
    UAH	Ukrainian Hryvnia	Ukraine
    TRY	Turkish Lira	Turkey"""
    bot.reply_to(message, reply_message)

@bot.message_handler(commands=['convert'])
def convert_handler(message):
    args = message.text.split(" ")
    if(len(args)-1 < 3):
        raise APIException(args,lambda err: bot.reply_to(message,err))

    answer = APIRequester.get_price(args[1],args[2],args[3])
    bot.reply_to(message, f"{args[3]} {args[1]} is {str(answer)} {args[2]}")

bot.infinity_polling()
