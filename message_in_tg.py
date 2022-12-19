import telebot
import random

bot = telebot.TeleBot('5666639146:AAH9H_x6TfmhITv8UAjb5rG3RzJTTPToTjs') # Создаем экземпляр бота

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    message = ''
    name_list = ['Кристина', 'Тигран', 'Корюн', 'Михаил']

    file_name = r'D:\Drafts\tg_bot\meeting_number.txt'
    with open(file_name, 'r') as file_object:
        round_number = int(file_object.read())

    bot.send_message(m.chat.id, f'Список на {round_number} - й круг заседания' +
                     ' клуба')

    round_number += 1
    with open(file_name, 'w') as file_object:
        file_object.write(str(round_number))

    random.shuffle(name_list)
    for name in name_list:
        message += '- ' + name + '\n'

    bot.send_message(m.chat.id, message)

# # Получение сообщений от юзера
# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     bot.send_message(message.chat.id, "Hello TG!\n It's python bot")

# Запускаем бота
bot.polling(none_stop=True, interval=0)