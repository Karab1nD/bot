import telebot
from telebot import types
from TaskProject import TaskOrganizer

TOKEN = '6858690220:AAEww7xoHHBGK4vtpS-WCrII1Vyei6L2igo'
bot = telebot.TeleBot(TOKEN)

organizer = TaskOrganizer()

main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add('📖 Все задачи', '⭐ Новая задача', '✅ Изменить задачу', '🪣 Удалить задачу')

main_kb_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_kb_cancel.add('Отмена')


@bot.message_handler(regexp='📖 Все задачи')
def show_tasks(message):
    tasks = organizer.view_tasks(message.chat.id)
    if tasks:
        for inx, task in enumerate(tasks, 1):
            mess = f'Номер: {inx}\n {task.title}\n {task.note}'
            print(mess)
            bot.send_message(message.chat.id, mess, reply_markup=main_kb, parse_mode="MarkdownV2")


@bot.message_handler(regexp='⭐ Новая задача')
def new_task(message):
    print(message)  # Ok, Dmitry, напиши название задачи
    bot.send_message(message.from_user.id, f'Ok, {message.from_user.first_name}, напиши название задачи',
                     reply_markup=main_kb_cancel)
    bot.register_next_step_handler(message, process_next_step1)


def process_next_step1(message):
    title = message.text.strip()
    if title.upper() == 'Отмена'.upper():
        bot.send_message(message.chat.id, 'Операция ввода отменена', reply_markup=main_kb)
        return
    bot.send_message(message.from_user.id, f'Ok, {message.from_user.first_name}, напиши описание задачи',
                     reply_markup=main_kb_cancel)
    bot.register_next_step_handler(message, process_next_step2, title)


def process_next_step2(message, title):
    note = message.text.strip()
    if note.upper() == 'Отмена'.upper():
        bot.send_message(message.chat.id, 'Операция ввода отменена', reply_markup=main_kb)
        return
    bot.send_message(message.from_user.id, f'Ok, {message.from_user.first_name}, напиши код',
                     reply_markup=main_kb_cancel)
    bot.register_next_step_handler(message, process_next_step3, title, note)


def process_next_step3(message, title, note):
    code = message.text.strip()
    if code.upper() == 'Отмена'.upper():
        bot.send_message(message.chat.id, 'Операция ввода отменена', reply_markup=main_kb)
        return
    organizer.add_task(message.chat.id, title, note)
    bot.send_message(message.chat.id, 'Задача успешно добавлена', reply_markup=main_kb)


@bot.message_handler(regexp='✅ Изменить задачу')
def upd_task(message):
    bot.send_message(message.from_user.id, f'Ok, {message.from_user.first_name}, напиши номер задачи',
                     reply_markup=main_kb_cancel)
    bot.register_next_step_handler(message, process_next_step_upd)


def process_next_step_upd(message):
    number = message.text.strip()
    if number.upper() == 'Отмена'.upper():
        bot.send_message(message.chat.id, 'Операция отменена', reply_markup=main_kb)
        return
    main_kb_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_kb_btn.add('Название', 'Описание', 'Код')
    main_kb_btn.row('Отмена')
    bot.send_message(message.from_user.id, f'Ok, {message.from_user.first_name}, что меняем?',
                     reply_markup=main_kb_btn)
    bot.register_next_step_handler(message, process_next_upd2, number)


def process_next_upd2(message, number):
    task = message.text.strip()
    if task.upper() == 'Отмена'.upper():
        bot.send_message(message.chat.id, 'Операция отменена', reply_markup=main_kb)
        return

    match task.upper():
        case 'НАЗВАНИЕ':
            mess = f'Ok, {message.from_user.first_name}, введите новое название?'
        case 'ОПИСАНИЕ':
            mess = f'Ok, {message.from_user.first_name}, введите новое описание?'
        case 'КОД':
            mess = f'Ok, {message.from_user.first_name}, введите новый код?'
        case _:
            mess = f'{message.from_user.first_name}, я тебя не понял, попробуй еще раз'
            bot.send_message(message.from_user.id, mess, reply_markup=main_kb)
            return

    bot.send_message(message.from_user.id, mess, reply_markup=main_kb_cancel)
    bot.register_next_step_handler(message, process_next_upd3, number, task)


def process_next_upd3(message, number, task):
    task2 = message.text.strip()
    if task2.upper() == 'Отмена'.upper():
        bot.send_message(message.chat.id, 'Операция отменена', reply_markup=main_kb)
        return

    match task.upper():
        case 'НАЗВАНИЕ':
            mess = f'Ok, {message.from_user.first_name}, название изменено'
            organizer.edit_title(message.chat.id, int(number), task2)
        case 'ОПИСАНИЕ':
            mess = f'Ok, {message.from_user.first_name}, описание изменено'
            organizer.edit_note(message.chat.id, int(number), task2)
        case 'КОД':
            mess = f'Ok, {message.from_user.first_name}, код изменен'
            organizer.edit_code(message.chat.id, int(number), task2)
    bot.send_message(message.chat.id, mess, reply_markup=main_kb)


@bot.message_handler(regexp='🪣 Удалить задачу')
def del_task(message):
    bot.send_message(message.from_user.id, f'Ok, {message.from_user.first_name}, напиши номер задачи',
                     reply_markup=main_kb_cancel)
    bot.register_next_step_handler(message, process_next_step_del)


def process_next_step_del(message):
    number = message.text.strip()
    if number.upper() == 'Отмена'.upper():
        bot.send_message(message.chat.id, 'Операция отменена', reply_markup=main_kb)
        return
    organizer.del_task(message.chat.id, int(number))
    bot.send_message(message.chat.id, 'Задача успешно удалена', reply_markup=main_kb)


@bot.message_handler(commands=['help', 'start'])
def start(message):
    organizer.save_user_data(message.chat.id, message.from_user.first_name, 1)
    commands_lst = [
        "/start - Старт",
        "/show_tasks - Список задач",
        "/add_task - Новая задача",
        "/update_task - Изменить задачу",
        "/delete_task - Удалить задачу"
    ]
    mess = "_Список доступных команд_"
    bot.send_message(message.chat.id, mess, reply_markup=main_kb, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, "\n".join(commands_lst), reply_markup=main_kb)


@bot.message_handler(commands=['del_task'])
def delete_task(message):
    bot.send_message(message.from_user.id, f'Ok, {message.from_user.first_name}, напиши номер задачи',
                     reply_markup=main_kb_cancel)
    bot.register_next_step_handler(message, process_next_step_del)


# админка
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id != 575489348:
        return

    users = organizer.read_users()

    inline_kb = types.InlineKeyboardMarkup()
    for userid, username in users:
        btn = types.InlineKeyboardButton(username, callback_data=userid)
        inline_kb.add(btn)
    bot.send_message(message.chat.id, 'Hi, Admin', reply_markup=inline_kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call)
    tasks = organizer.view_tasks(call.data)
    if tasks:
        for inx, task in enumerate(tasks, 1):
            mess = f'Номер: {inx}\n {task.title}\n {task.note}'
            bot.send_message(call.from_user.id, mess, parse_mode="MarkdownV2")


bot.polling(none_stop=True)
