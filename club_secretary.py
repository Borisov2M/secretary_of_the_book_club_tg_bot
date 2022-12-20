import re
import time 
import random
import telebot  

from telebot import types

bot = telebot.TeleBot('5666639146:AAH9H_x6TfmhITv8UAjb5rG3RzJTTPToTjs') # Создаем экземпляр бота

global name_list_path
global meeting_number_path

name_list_path = r'D:\Drafts\tg_bot\name_list.txt'
meeting_number_path = r'D:\Drafts\tg_bot\meeting_number.txt'

#*********************** Работа с членами книжного клуба ***********************
#-- Рандомизация списка членов клуба для создания очередности предложения книг -
@bot.message_handler(commands=["random"])
def randomize_names(m, res=False):
    message = ''
    name_list = []

    with open(name_list_path, 'r') as name_file_object: # , encoding='utf-8'
        for name in name_file_object:
            if '\n' in name:
                name = re.sub('\n', '', name)
            name_list.append(name)

    with open(meeting_number_path, 'r') as number_file_object:
        round_number = int(number_file_object.read())

    message = (f'Список на {round_number} - й круг заседания' +
                     ' клуба\n')

    round_number += 1
    with open(meeting_number_path, 'w') as number_file_object:
        number_file_object.write(str(round_number))

    random.shuffle(name_list)
    for name in name_list:
        message += '     - ' + name + '\n'

    bot.send_message(m.chat.id, message)
#-------------------------------------------------------------------------------

#---------------------- Вывод списка членов книжного клуба ---------------------
@bot.message_handler(commands=["view"])
def view_member_list(m, res=False):
    list_name_message = 'Список членов клуба:\n'
    with open(name_list_path, 'r') as name_file_object:
        for name in name_file_object:
            list_name_message += '     - ' + name
    
    bot.send_message(m.chat.id, list_name_message)
#-------------------------------------------------------------------------------

#------------------- Добавление новых членов книжного клуба --------------------
@bot.message_handler(commands=["add"])
def neofit(m, res=False):
    sent = bot.send_message(m.chat.id, 'Введите имя новопосвященного!')
    bot.register_next_step_handler(sent, add_neofit)

def add_neofit(m, res=False):
    with open(name_list_path, 'a') as name_file_object:
        name_file_object.write('\n' + m.text)
    message = 'Неофит добавлен в список'
    bot.send_message(m.chat.id, message)
#-------------------------------------------------------------------------------

#------------------- Удаление из списка членов книжного клуба ------------------
@bot.message_handler(commands=["delete"])
def member(m, res=False):
    view_member_list(m)
    sent = bot.send_message(m.chat.id, 'Введите имя отступника!')
    bot.register_next_step_handler(sent, delete_member)

def delete_member(m, res=False):
    with open(name_list_path, 'r') as name_file_object: 
        name_list = name_file_object.readlines()

    with open(name_list_path, 'w') as name_file_object:
        for name in name_list:
            if name != m.text:
                name_file_object.write(name)
                
    message = 'Отступник стерт из хроник!'
    bot.send_message(m.chat.id, message)
#-------------------------------------------------------------------------------
#*******************************************************************************

@bot.message_handler(commands=["booklist"])
def neofit(m, res=False):
    sent = bot.send_message(m.chat.id, 'Введите название книги!')
    bot.register_next_step_handler(sent, add_book_name)

def add_book_name(m, res=False):
    with open(name_list_path, 'a') as book_file_object:
        book_file_object.write('\n' + m.from_user.username + ': ' + m.text)
    message = 'Книга добавлена в список'
    bot.send_message(m.chat.id, message)

@bot.message_handler(commands=["hello","привет"])
def hello(m, res=False):
    t = time.localtime() 
    current_time = int(time.strftime("%H", t))

    if current_time in range(4, 12):
        message = ('Хорошее утро, ' + m.from_user.first_name + ' ' 
                                    + m.from_user.last_name +'!')
    elif current_time in range(12, 18):
        message = ('Хороший день, ' + m.from_user.first_name + ' ' 
                                    + m.from_user.last_name +'!')
    elif current_time in range(18, 19):
        message = ('Хороший вечер, ' + m.from_user.first_name + ' ' 
                                     + m.from_user.last_name +'!')
    else:
        message = ('Хорошая ночь, ' + m.from_user.first_name + ' ' 
                                    + m.from_user.last_name +'!')

    bot.send_message(m.chat.id, message)

@bot.message_handler(commands=["help", "что_ты_можешь"])
def help(m, res=False):
    message = '/view - показать список членов клуба\n'
    message += '/random - жребий очередности выбора\n'
    message += '/add - добавить неофита\n'
    message += '/delete - удалить члена клуба\n'
    message += '/hello - поздороваться\n'
    message += '/help - список команд'
    bot.send_message(m.chat.id, message)

# Запускаем бота
bot.polling(none_stop=True, interval=0)