#create venv
virtualenv venv
source venv/bin/activate
deactivate

#save packages in requirements.txt
pip3 freeze > requirements.txt

#install packages from requirements.txt
pip3 install -r requirements.txt

#bot send message
# -*- coding: utf-8 -*-
import config
import telebot

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)

vXdG8jnB9DuV38w7