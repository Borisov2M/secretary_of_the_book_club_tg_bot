import re
import time 
import random
import telebot  

from telebot import types

bot = telebot.TeleBot('5666639146:AAH9H_x6TfmhITv8UAjb5rG3RzJTTPToTjs') # Создаем экземпляр бота

global name_list_path
global book_list_path
global rule_book_path
global meeting_number_path

name_list_path = r'D:\Drafts\tg_bot\name_list.txt'
rule_book_path = r'D:\Drafts\tg_bot\rule_book.txt'
book_list_path = r'D:\Drafts\tg_bot\book_list.txt'
meeting_number_path = r'D:\Drafts\tg_bot\meeting_number.txt'

#*********************** Работа с членами книжного клуба ***********************
#-- Рандомизация списка членов клуба для создания очередности предложения книг -
@bot.message_handler(commands=["randomize_members"])
def randomize_names(m, res=False):
    message = ''
    name_list = []

    with open(name_list_path, 'r') as name_file_object: # , encoding='utf-8'
        for name in name_file_object:
            if '\n' in name:
                name = re.sub('\n', '', name)
            name_list.append(name)
    name_file_object.close()

    with open(meeting_number_path, 'r') as number_file_object:
        round_number = int(number_file_object.read())
    number_file_object.close()

    message = (f'Список на {round_number} - й круг заседания' +
                     ' клуба\n')
    round_number += 1

    with open(meeting_number_path, 'w') as number_file_object:
        number_file_object.write(str(round_number))
    number_file_object.close()

    random.shuffle(name_list)
    for name in name_list:
        message += '     - ' + name + '\n'

    bot.send_message(m.chat.id, message)
#-------------------------------------------------------------------------------

#---------------------- Вывод списка членов книжного клуба ---------------------
@bot.message_handler(commands=["members_list"])
def view_member_list(m, res=False):
    list_name_message = 'Список членов клуба:\n'
    with open(name_list_path, 'r') as name_file_object:
        for name in name_file_object:
            list_name_message += '     - ' + name
    
    name_file_object.close()

    bot.send_message(m.chat.id, list_name_message)
#-------------------------------------------------------------------------------

#------------------- Добавление новых членов книжного клуба --------------------
@bot.message_handler(commands=["add_neofit"])
def neofit(m, res=False):
    bot.send_message(m.chat.id, "Ввод начинается с символа '/'")
    sent = bot.send_message(m.chat.id, 'Введите имя новопосвященного!')
    bot.register_next_step_handler(sent, add_neofit)

def add_neofit(m, res=False):
    if m.from_user.id:
        with open(name_list_path, 'a') as name_file_object:
            name_file_object.write(m.text[1:] + '\n')
        bot.send_message(m.chat.id, 'Неофит добавлен в список')
        name_file_object.close()
#-------------------------------------------------------------------------------

#------------------- Удаление из списка членов книжного клуба ------------------
@bot.message_handler(commands=["delete_member"])
def member(m, res=False):
    bot.send_message(m.chat.id, "Ввод начинается с символа '/'")
    view_member_list(m)
    sent = bot.send_message(m.chat.id, 'Введите имя отступника!')
    bot.register_next_step_handler(sent, member_delete)

def member_delete(m, res=False):
    with open(name_list_path, 'r') as name_file_object: 
        name_list = name_file_object.readlines()
    name_file_object.close()
    delete_name = m.text[1:]
        
    with open(name_list_path, 'w') as name_file_object:
        for name in name_list:
            if '\n' in name:
                plug = re.sub('\n', '', name)
            else:
                plug = name

            if plug != m.text[1:] :
                name_file_object.write(name)

    name_file_object.close    
    bot.send_message(m.chat.id, 'Отступник стерт из хроник!')
#-------------------------------------------------------------------------------
#*******************************************************************************

#*************************** Блотк работы с книгами ****************************
#-------------------- Добавление новых книг книжного клуба ---------------------
@bot.message_handler(commands=["add_book"])
def new_book(m, res=False):
    bot.send_message(m.chat.id, "Ввод начинается с символа '/'")
    sent = bot.send_message(m.chat.id, 'Введите название книги!')
    bot.register_next_step_handler(sent, add_book_name)

def add_book_name(m, res=False):
    with open(book_list_path, 'a') as book_file_object:
        book_file_object.write(m.from_user.username  + ': ' + m.text[1:] + '\n')
    bot.send_message(m.chat.id,'Книга поставлена на полку')

    book_file_object.close()
#-------------------------------------------------------------------------------

#------------- Удаление из списка прочитанных книг книжного клуба --------------
@bot.message_handler(commands=["delete_book"])
def book(m, res=False):
    bot.send_message(m.chat.id, "Ввод начинается с символа '/'")
    view_book_list(m)
    sent = bot.send_message(m.chat.id, 'Введите название книги!')
    bot.register_next_step_handler(sent, book_delete)

def book_delete(m, res=False):
    with open(book_list_path, 'r') as book_file_object:     
        book_list = book_file_object.readlines()
    
    book_file_object.close()
        
    with open(book_list_path, 'w') as book_file_object:
        for book in book_list:
            if '\n' in book:
                plug = re.sub('\n', '', book)
            else:
                plug = book

            if plug != (m.from_user.username + ': ' + m.text[1:]) :
                book_file_object.write(book)

    book_file_object.close
    bot.send_message(m.chat.id, 'Книга убрана из библиотеки!')
#-------------------------------------------------------------------------------

#--------------------- Вывод списка прочитанных книг клуба ---------------------
@bot.message_handler(commands=["books_list"])
def view_book_list(m, res=False):
    list_book_message = 'Список прочитанных книг:\n'
    with open(book_list_path, 'r') as book_file_object:
        for name in book_file_object:
            list_book_message += '     - ' + name
    
    book_file_object.close()
    bot.send_message(m.chat.id, list_book_message)
#-------------------------------------------------------------------------------
#*******************************************************************************

#---------------------- Вывод списка правил книжного клуба ---------------------
@bot.message_handler(commands=["rule_book"])
def view_rule_book(m, res=False):
    rule_book_message = 'Список правил клуба:\n'
    with open(rule_book_path, 'r', encoding='utf-8') as rule_book_object:
        for rule in rule_book_object:
            rule_book_message += '     ' + rule
    
    rule_book_object.close()
    bot.send_message(m.chat.id, rule_book_message)
#-------------------------------------------------------------------------------

#------------------------ Сказать привет секретарю клуба -----------------------
@bot.message_handler(commands=["hello","привет"])
def hello(m, res=False):
    t = time.localtime() 
    current_time = int(time.strftime("%H", t))

    if current_time in range(4, 12):
        message = ('Хорошее утро, ' + str(m.from_user.username) + '!')
    elif current_time in range(12, 18):
        message = ('Хороший день, ' + str(m.from_user.username) + '!')
    elif current_time in range(18, 19):
        message = ('Хороший вечер, ' + str(m.from_user.username) + '!')
    else:
        message = ('Хорошая ночь, ' + str(m.from_user.username) + '!')

    bot.send_message(m.chat.id, message)
#-------------------------------------------------------------------------------

#---------------------- Список команд для работы секретаря ---------------------
@bot.message_handler(commands=["help", "подсказка"])
def help(m, res=False):
    message = '/randomize_members - жребий очередности выбора\n'
    message += '/add_neofit - добавить неофита\n'
    message += '/delete_member - удалить члена клуба\n'
    message += '/members_list - показать список членов клуба\n'
    message += '/add_book - добавить книгу\n'
    message += '/delete_book - удалить книгу\n'
    message += '/books_list - показать список книг\n'
    message += '/rule_book - показать книгу правил клуба\n'
    message += '/hello - поздороваться\n'
    message += '/help - подсказка'
    bot.send_message(m.chat.id, message)
#-------------------------------------------------------------------------------

# Запускаем бота
bot.polling(none_stop=True, interval=0)