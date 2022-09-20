#import google.cloud.logging
#client = google.cloud.logging.Client()
#client.setup_logging()
import logging
import os
import threading
import time
from datetime import datetime, timedelta, date
import telebot
from telebot import types
from typing import List
import json
from classes.MainResolver import MainResolver, WeekDayResolver
from classes.UserData import UserData
from helpers.helpers import get_week_num, getDecodedSchedule, getNextSaturdayDate, getSaturdayData, getClassesStr

token = os.getenv('TOKEN_BOT')
# bot init
bot = telebot.TeleBot(token)
user_dict = {}
watching_users_list_by_group = {1: [], 2: []}
users_id_to_sent_message = []


def startMonitoring():
    try:
        while True:
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                print(now)
                todays_date = date.today()
                week_num = get_week_num(todays_date.day, todays_date.month, todays_date.year)
                is_found = False
                for group_num in watching_users_list_by_group:
                    week_schedule = MainResolver(getDecodedSchedule(group_num))
                    week = week_schedule.getWeekByNumber(week_num)
                    saturday_lessons = getSaturdayLessonsIfToday(group_num, date.today())['objects']
                    day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(todays_date.weekday())) if not saturday_lessons else saturday_lessons
                    for clas in day_classes:
                        clas_time = str(clas.getTime()[0])
                        if str(clas_time) == str(current_time):
                            is_found = True
                            for user in watching_users_list_by_group[group_num]:
                                try:
                                    bot.send_message(user.id, "Через 5 хв почнеться пара:\n" + str(clas), disable_notification=bool(not clas.should_be_visited), parse_mode="html", disable_web_page_preview=True)
                                except Exception as e:
                                    logging.error("seems like user blocked bot!! ||user: "+str(user.id)+"error:" + str(e))
                if is_found:
                    time.sleep(50)  # TODO:set 1500
            except Exception as e:
                logging.error("Error in MONITORING while loop!! error:" + str(e))
            time.sleep(11)
    except Exception as e:
        logging.error("MONITORING IS BROKEN!! error:" + str(e))

t = threading.Thread(target=startMonitoring)
t.start()

def sendLogError(user_id, func_name, error, user_input=""):
    try:
        user = user_dict[user_id].user_name
        logging.error('user:' + str(user) + ' || func_name:' + str(func_name) + ' ||user_input:' + str(user_input)+ ' ||error:' + str(error))
    except Exception:
        logging.error('someone without id tried to break me :(')
        pass


def isUserInMonitoringList(user):
    result = False
    try:
        user_group = user.selected_group
        result = user in watching_users_list_by_group[user_group]
    except Exception as e:
        sendLogError(user.id, 'isUserInMonitoringList', e)
        print("error in isUserInMonitoringList" + str(e))
    return result

def addUserToMonitoringList(user_id):
    user = user_dict[user_id]
    if not isUserInMonitoringList(user):
        watching_users_list_by_group[user.selected_group].append(user)

def removeUserToMonitoringList(user_id):
    user = user_dict[user_id]
    if isUserInMonitoringList(user):
        watching_users_list_by_group[user.selected_group].remove(user)

def setUserActivity(user_id, activity_name):
    try:
        if user_id not in user_dict:
            return False
        else:
            user = user_dict[user_id]
            if activity_name in user.activity_list.keys():
                user.activity_list[activity_name] += 1
            else:
                user.activity_list[activity_name] = 1
    except Exception as e:
        print('error while setting activity:' + str(e))
        pass

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1", "2")
    msg = bot.send_message(message.chat.id,
                           "Привіт ✌️, я бот-помічник. \nМожу: \n    надсилати час до найближчої пари\n    повідомляти про початок пари за 5хв(моніторинг)\n    показати список пар в найближчу суботу  \nВведіть номер своєї підгрупи (1/2):",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, process_group_step)


def process_group_step(message):
    try:
        setUserActivity(message.chat.id, 'process_group_step')
        if message.text == '1' or message.text == '2':
            is_old_user = message.chat.id in user_dict
            if is_old_user and isUserInMonitoringList(user_dict[message.chat.id]):
                removeUserToMonitoringList(message.chat.id)
                user_dict[message.chat.id].selected_group = int(message.text)
                addUserToMonitoringList(message.chat.id)
            else:
                try:
                    username = message.from_user.username
                    username = username if username is not None else message.from_user.first_name
                    username = username if username is not None else 'undefined username:' + message.chat.id
                except Exception as e:
                    username = 'undefined username' + message.chat.id
                user_data = UserData(int(message.chat.id), int(message.text), username)
                user_dict[message.chat.id] = user_data
                addUserToMonitoringList(message.chat.id)
            go_to_process_schedule_step_1(message,
                                          f'Відстежується {message.text} підгруппа, виберіть наступну дію:')
        else:
            msg = bot.reply_to(message, 'Невірний номер підгрупи! Введіть ще раз:')
            bot.register_next_step_handler(msg, process_group_step)
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'process_group_step', e, message)
        msg = bot.reply_to(message, 'Щось пішло не так :( спробуй знову')
        bot.register_next_step_handler(message, start_message)


def menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Сьогодні', 'Завтра')
    markup.add('Обрати за днем тижня', 'Фото Розкладу')
    markup.add("Назад👈", "Зміна підгрупи♻")
    return markup


def process_schedule_step_1(message):
    try:
        setUserActivity(message.chat.id, 'process_schedule_step_1('+message.text+')')
        if message.text == 'Переглянути розклад':
            msg = bot.send_message(message.chat.id, 'Виберіть один із запропонованих варіантів:', reply_markup=menu())
            bot.register_next_step_handler(msg, process_schedule_step_2)
        elif message.text == 'Запустити Моніторинг':
            addUserToMonitoringList(message.chat.id)
            go_to_process_schedule_step_1(message, 'Моніторю розклад. Тепер бот буде надсилати сповіщення за 5 хв до початку пари😉')
        elif message.text == 'Зупинити Моніторинг':
            removeUserToMonitoringList(message.chat.id)
            go_to_process_schedule_step_1(message, 'Закінчив моніторити')
        elif message.text == 'Пари в суботу':
            result_message = getSaturdayLessonsIfToday(user_dict[message.chat.id].selected_group, getNextSaturdayDate())['reply']
            if not result_message:
                result_message = 'схоже на цюю суботу нічого не перенесли'
            go_to_process_schedule_step_1(message, result_message)
        elif message.text == 'Назад👈':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("1", "2")
            msg = bot.send_message(message.chat.id, 'Введіть номер своєї підгрупи (1/2):', reply_markup=markup)
            bot.register_next_step_handler(msg, process_group_step)
        elif message.text == "Наступна пара":
            main_resolver = MainResolver(getDecodedSchedule(user_dict[message.chat.id].selected_group))
            saturday_data = getSaturdayData(date.today())
            next_class = main_resolver.getNextClass(None if not saturday_data else saturday_data['week_num'], None if not saturday_data else saturday_data['day_name'])
            if next_class is None:
                msg = bot.send_message(message.chat.id, 'Більше пар сьогодні не буде')
            else:
                msg = bot.send_message(message.chat.id, "наступна пара: (до початку " + next_class['time_left'] + ")\n" + str(next_class['object']), parse_mode="html", disable_web_page_preview=True)
            bot.register_next_step_handler(msg, process_schedule_step_1)
        elif message.from_user.id == 608787896 and message.text == 'admin':
            go_to_admin_panel()
        else:
            msg = bot.send_message(message.chat.id, 'Невірний вибір! Спробуйте ще раз:')
            bot.register_next_step_handler(msg, process_schedule_step_1)
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'process_schedule_step_1', e, message)
        bot.reply_to(message, 'Щось пішло не так :(1')
        bot.register_next_step_handler(message, process_schedule_step_1)


def handle_admin(message):
    try:
        if message.text == "Статистика":
            static_msg = 'user_count:' + str(len(user_dict))
            static_msg += '\nuser_mon_g_1:' + str(len(watching_users_list_by_group[1]))
            static_msg += '\nuser_mon_g_2:' + str(len(watching_users_list_by_group[2]))
            static_msg += '\nusers:'
            count = 1
            for user_id in user_dict:
                user = user_dict[user_id]
                if user is None:
                    continue
                static_msg += '\n   ' + str(count) + ') name:' + str(user.user_name) + '   gr:' + str(
                    user.selected_group) + '   in_mon_list:' + str(isUserInMonitoringList(user)) + ' id:'+ str(user.id)
                count += 1
                for activity in user.activity_list.keys():
                    static_msg += '\n      ' + str(user.activity_list[activity]) + ': ' + str(activity)
            go_to_admin_panel('ну держи\n' + static_msg)
            logging.info('чел з айді глянув статистику ' + str(message.chat.id))
        elif message.text == "Послать меседж юзерам":
            msg = bot.send_message(message.chat.id, 'Введи повідомлення:')
            bot.register_next_step_handler(msg, sent_message_to_users)
        elif message.text == "Послать меседж юзерам по айди":
            msg = bot.send_message(message.chat.id, 'Введи юзер айдишніки:')
            bot.register_next_step_handler(msg, sent_message_to_users_set_id)
        elif message.text == "Список юзеров":
            users = ''
            for user_id in user_dict:
                users += str(user_id) + ','
            go_to_admin_panel('список юзеров\n' + users)
        elif message.text == "Змінити розклад":
            msg = bot.send_message(message.chat.id, 'Скинь файл розпорядку:')
            bot.register_next_step_handler(msg, update_schedule_handler)
        elif message.text == 'Очистити активність':
            try:
                for user_id in user_dict:
                    user = user_dict[user_id]
                    if user is None:
                        continue
                    user.activity_list = {}
            except Exception as e:
                sendLogError(608787896, 'Очистити активність', e, '')
            go_to_admin_panel()
        else:
            go_to_process_schedule_step_1(message)
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'sent_message_to_users', e, message)
        msg = bot.reply_to(message, 'Щось пішло не так :( спробуй знову')
        go_to_admin_panel()


@bot.message_handler(content_types=['document'])
def update_schedule_handler(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('static/schedule1.json', 'wb') as new_file:
            new_file.write(downloaded_file)
        print(getDecodedSchedule(1))

        bot.send_message(608787896, "апдейтнув розклад")
        go_to_admin_panel()
    except Exception as e:
        bot.send_message(608787896, "ошибка коли апдейтив розклад")
        sendLogError(608787896, 'update_schedule_handler', e, 'file')
        go_to_admin_panel()


def sent_message_to_users(message):
    try:
        if message != 'no':
            for user_id in user_dict:
                try:
                    bot.send_message(user_id, message.text, disable_notification=False)
                except Exception as e:
                    bot.reply_to(message, 'не зміг послать меседж юзеру ' + str(user_id) + ' ' + str(user_dict[user_id].user_name))
                    sendLogError(message.chat.id, 'sent_message_to_users for loop', e, message)
        go_to_admin_panel()
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'sent_message_to_users', e, message)
        msg = bot.reply_to(message, 'Щось пішло не так :( спробуй знову')
        go_to_admin_panel()
def sent_message_to_users_by_id(message):
    try:
        if message.text != 'no':
            for user_id in users_id_to_sent_message:
                try:
                    bot.send_message(user_id, message.text)
                except Exception as e:
                    user_name = "undefined_user" if user_id not in user_dict else str(user_dict[user_id].user_name)
                    bot.reply_to(message, 'не зміг послать меседж юзеру ' + str(user_id) + ' ' + user_name)
                    sendLogError(message.chat.id, 'sent_message_to_users_by_id for loop', e, message)
        go_to_admin_panel()
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'sent_message_to_users_by_id', e, message)
        msg = bot.reply_to(message, 'Щось пішло не так :( спробуй знову')
        go_to_admin_panel()
def sent_message_to_users_set_id(message):
    try:
        global users_id_to_sent_message
        users_id_to_sent_message = json.loads('['+message.text+']')
        msg = bot.send_message(message.chat.id, 'Введи повідомлення:')
        bot.register_next_step_handler(msg, sent_message_to_users_by_id)
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'sent_message_to_users', e, message)
        msg = bot.reply_to(message, 'Щось пішло не так :( спробуй знову')
        go_to_admin_panel()

def getSaturdayLessonsIfToday(selected_group, day):
    reply = ''
    day_classes = []
    try:
        saturday_data = getSaturdayData(day)
        if saturday_data:
            reply += "відпрацьовуєм за " + str(saturday_data['postponed_from']) + (' II' if saturday_data['week_num'] %2 == 0 else ' I') + ' тиждень ' + ' ' + str(saturday_data['day_name']) + '\n'
            obj = MainResolver(getDecodedSchedule(selected_group))
            week = obj.getWeekByNumber(saturday_data['week_num'])
            day_classes = week.getDayClassesByDayName(saturday_data['day_name'])
            reply += getClassesStr(day_classes)
    except Exception as e:
        logging.error("func: getSaturdayLessonsIfToday")
    return {"reply": reply, "objects": day_classes}

def process_schedule_step_2(message):
    try:
        setUserActivity(message.chat.id, 'process_schedule_step_2(' + message.text + ')')
        if message.text == 'Сьогодні':
            bot.send_message(message.chat.id, 'Розклад на сьогодні')
            todays_date = date.today()
            week_num = get_week_num(todays_date.day, todays_date.month, todays_date.year)
            user_data = user_dict[message.chat.id]  # група
            obj = MainResolver(getDecodedSchedule(user_data.selected_group))
            week = obj.getWeekByNumber(week_num)
            day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(todays_date.weekday()))
            reply = ''
            for clas in day_classes:
                reply += str(clas) + '\n'
            saturday_lessons = getSaturdayLessonsIfToday(user_dict[message.chat.id].selected_group, date.today())['reply']
            msg = bot.send_message(message.chat.id, reply if not saturday_lessons else saturday_lessons, parse_mode="html", disable_web_page_preview=True)
            bot.register_next_step_handler(msg, process_schedule_step_2)

        elif message.text == 'Завтра':
            bot.send_message(message.chat.id, 'Розклад на завтра')
            todays_date = date.today()
            tomorrow_date = todays_date + timedelta(days=1)
            week_num = get_week_num(tomorrow_date.day, tomorrow_date.month, tomorrow_date.year)
            user_data = user_dict[message.chat.id]  # група
            obj = MainResolver(getDecodedSchedule(user_data.selected_group))
            week = obj.getWeekByNumber(week_num)
            day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(tomorrow_date.weekday()))
            if not day_classes:
                saturday_lessons = getSaturdayLessonsIfToday(user_dict[message.chat.id].selected_group, timedelta(days=1) + date.today())['reply']
                msg = bot.send_message(message.chat.id, 'Пар немає.' if not saturday_lessons else saturday_lessons, parse_mode="html", disable_web_page_preview=True)
                bot.register_next_step_handler(msg, process_schedule_step_2)
            else:
                reply = ''
                for clas in day_classes:
                    reply += str(clas) + '\n'
                msg = bot.send_message(message.chat.id, reply, parse_mode="html", disable_web_page_preview=True)
                bot.register_next_step_handler(msg, process_schedule_step_2)

        elif message.text == 'Обрати за днем тижня':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            first_week_option = '1'
            second_week_option = '2'
            todays_date = date.today()
            if get_week_num(todays_date.day, todays_date.month, todays_date.year) == 1:
                first_week_option += '(Поточний)'
            else:
                second_week_option += '(Поточний)'
            markup.add(first_week_option, second_week_option)
            markup.add("Назад👈")
            msg = bot.send_message(message.chat.id, 'Оберіть тиждень:', reply_markup=markup)
            bot.register_next_step_handler(msg, process_schedule_step_3)
        elif message.text == 'Фото Розкладу':
            today_date = date.today()
            week_num = get_week_num(today_date.day, today_date.month, today_date.year)
            day_name = WeekDayResolver.getDayNameByNumber(datetime.today().weekday())
            message_to_sent = "Сьогодні " + day_name + ", " + str(week_num) + "-й тиждень"
            msg = bot.send_message(message.chat.id, message_to_sent)
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open('media/photo_1.jpg', 'rb')), telebot.types.InputMediaPhoto(open('media/photo_2.jpg', 'rb'))])
            bot.register_next_step_handler(msg, process_schedule_step_2)
        elif message.text == "Назад👈":
            go_to_process_schedule_step_1(message)
        elif message.text == 'Зміна підгрупи♻':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("1", "2")
            msg = bot.send_message(message.chat.id, 'Введіть номер своєї підгрупи (1/2):',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, process_group_step)
        else:
            if message.text != "Назад👈" or message.text != 'Зміна підгрупи♻':
                msg = bot.send_message(message.chat.id, 'Невірний вибір! Спробуйте ще раз:')
                bot.register_next_step_handler(msg, process_schedule_step_2)
            else:
                msg = bot.send_message(message.chat.id, 'Виберіть один із запропонованих варіантів:',
                                       reply_markup=menu())
                bot.register_next_step_handler(msg, process_schedule_step_2)
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'process_schedule_step_2', e, message)
        msg = bot.reply_to(message, 'Вихідний!!! Що будемо робити далі?')
        bot.register_next_step_handler(msg, process_schedule_step_2)


def go_to_admin_panel(message_to_sent='Вибери дію:'):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Статистика", "Список юзеров", "Очистити активність")
    markup.add("Послать меседж юзерам по айди", "Послать меседж юзерам", "Змінити розклад")
    markup.add("Назад")
    msg = bot.send_message(608787896, message_to_sent, reply_markup=markup)
    bot.register_next_step_handler(msg, handle_admin)

def go_to_process_schedule_step_1(message, text_to_sent: str = 'Виберіть наступну дію:'):
    try:
        isAdmin = message.from_user.id == 608787896
        user = user_dict[message.chat.id]
        is_user_monitoring_active = user in watching_users_list_by_group[user.selected_group]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Переглянути розклад", "Зупинити Моніторинг" if is_user_monitoring_active else "Запустити Моніторинг")
        markup.add("Наступна пара", "Пари в суботу")
        markup.add("Назад👈")
        if isAdmin:
            markup.add("admin")
        msg = bot.send_message(message.chat.id, text_to_sent,
                               reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
        bot.register_next_step_handler(msg, process_schedule_step_1)
    except Exception as e:
        sendLogError(message.chat.id, 'go_to_process_schedule_step_1', e, message)
        print('err')

def process_schedule_step_3(message):
    try:
        setUserActivity(message.chat.id, 'process_schedule_step_3(' + message.text + ')')
        if message.text == "Назад👈":
            msg = bot.send_message(message.chat.id, 'Виберіть один із запропонованих варіантів:', reply_markup=menu())
            bot.register_next_step_handler(msg, process_schedule_step_2)
        elif message.text == "1(Поточний)" or message.text == "2(Поточний)" or message.text == "1" or message.text == "2":
            week = message.text
            user_data = user_dict[message.chat.id]
            user_data.selected_week = int(week[0])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця')
            markup.add("Головне меню👈")
            msg = bot.send_message(message.chat.id, 'Оберіть день:', reply_markup=markup)
            bot.register_next_step_handler(msg, process_schedule_step_4)
        else:
            msg = bot.send_message(message.chat.id, 'Невірний вибір! Оберіть тиждень:')
            bot.register_next_step_handler(msg, process_schedule_step_3)
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'process_schedule_step_3', e, message)
        bot.reply_to(message, 'Щось пішло не так :(3')
        bot.register_next_step_handler(message, process_schedule_step_3)


def process_schedule_step_4(message):
    try:
        setUserActivity(message.chat.id, 'process_schedule_step_4(' + message.text + ')')
        if message.text == "Головне меню👈":
            msg = bot.send_message(message.chat.id, 'Виберіть один із запропонованих варіантів:', reply_markup=menu())
            bot.register_next_step_handler(msg, process_schedule_step_2)
        elif message.text == "Понеділок" or message.text == "Вівторок" or message.text == "Середа" or message.text == "Четвер" or message.text == "Пятниця":
            day = message.text
            user_data = user_dict[message.chat.id]
            user_data.selected_day = str(day)
            obj = MainResolver(getDecodedSchedule(user_data.selected_group))
            week = obj.getWeekByNumber(user_data.selected_week)
            day_classes = week.getDayClassesByDayName(user_data.selected_day)
            if not day_classes:
                msg = bot.send_message(message.chat.id, 'Пар немає. Оберіть день:')
                bot.register_next_step_handler(msg, process_schedule_step_4)
            else:
                reply = ''
                for clas in day_classes:
                    reply += str(clas) + '\n'
                bot.send_message(message.chat.id, reply, parse_mode="html", disable_web_page_preview=True)
                msg = bot.send_message(message.chat.id, 'Оберіть день:')
                bot.register_next_step_handler(msg, process_schedule_step_4)
        else:
            msg = bot.send_message(message.chat.id, 'Невірний вибір! Оберіть день:')
            bot.register_next_step_handler(msg, process_schedule_step_4)
    except Exception as e:
        print(e)
        sendLogError(message.chat.id, 'process_schedule_step_4', e, message)
        bot.reply_to(message, 'Щось пішло не так :(4')
        bot.register_next_step_handler(message, process_schedule_step_4)


if __name__ == "__main__":
    bot.infinity_polling()
