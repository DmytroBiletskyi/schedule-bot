import calendar
import os
import time
from datetime import datetime, timedelta, date
import telebot
from telebot import types
from typing import List
import json

token = os.getenv('TOKEN_BOT')

# bot init
bot = telebot.TeleBot(token)
user_dict = {}
is_watching = True


def getDecodedSchedule(search_group=1):
    schedule_arr = {}
    json_string = '{ "groups": [ { "group_number": 1, "weeks": [ { "week_number": 1, "week_days": [ { "day_name": "Понеділок", "classes": [ { "number": 3, "name": "(Лабораторна) Управління інформаційною безпекою: Коломієць М.В.", "shouldBeVisited": false, "meetLink": "https://meet.google.com/uat-bmtm-msk" }, { "number": 4, "name": "(Лабораторна) Захищені компютерні сист та  мережі: Кривокульська О.О.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 5, "name": "(Практична) Організаційне забезпечення захисту ін.: Телющенко В.А.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/xfq-pzav-vse" }, { "number": 6, "name": "(Лабораторна) Операційні сист та технолог їх захисту: Карабань М.В.", "shouldBeVisited": false, "meetLink": "-" } ] }, { "day_name": "Вівторок", "classes": [ { "number": 3, "name": "(Лекція) Прикладна криптологія: Ільєнко А.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/nsh-htkt-zdj" }, { "number": 4, "name": "(Лекція) Захищені компютерні сист та  мережі: Єлізаров А.Б.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/xud-mqci-ovg" } ] }, { "day_name": "Середа", "classes": [] }, { "day_name": "Четвер", "classes": [ { "number": 4, "name": "(Лекція) Організаційне забезпечення захисту ін.: Петренко А.Б.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 5, "name": "(Лекція) Ліцензування та сертифік у сф зах інф: Хорошко В.О.", "shouldBeVisited": false, "meetLink": "-" } ] }, { "day_name": "Пятниця", "classes": [ { "number": 3, "name": "(Лекція) Управління інформаційною безпекою: Казмірчук С.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/jjy-vxyo-nsa" }, { "number": 4, "name": "(Лекція) Операційні сист та технолог їх захисту: Гулак Н.К.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/deb-rcae-bwm" } ] } ] }, { "week_number": 2, "week_days": [ { "day_name": "Понеділок", "classes": [ { "number": 3, "name": "(Лабораторна) Прикладна криптологія: Прокопенко О.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/rtd-unck-zbj" }, { "number": 4, "name": "(Лабораторна) Прикладна криптологія: Прокопенко О.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/rtd-unck-zbj" }, { "number": 5, "name": "(Лабораторна) Ліцензування та сертифік у сф зах інф: Хохлачева Ю.Є.", "shouldBeVisited": false, "meetLink": "-" } ] }, { "day_name": "Вівторок", "classes": [ { "number": 3, "name": "(Лекція) Прикладна криптологія: Ільєнко А.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/nsh-htkt-zdj" }, { "number": 4, "name": "(Лекція) Захищені компютерні сист та  мережі: Єлізаров А.Б.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/xud-mqci-ovg" } ] }, { "day_name": "Середа", "classes": [] }, { "day_name": "Четвер", "classes": [ { "number": 2, "name": "(Лабораторна) Авіаційна безп та кібербез авіац інф сис: Іванченко І.С.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/vhr-ucpf-pwq" }, { "number": 3, "name": "(Лабораторна) Авіаційна безп та кібербез авіац інф сис: Іванченко І.С.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/vhr-ucpf-pwq" }, { "number": 4, "name": "(Лекція) Організаційне забезпечення захисту ін.: Петренко А.Б.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 5, "name": "(Лекція) Авіаційна безп та кібербез авіац інф сис: Іванченко Є.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/vhr-ucpf-pwq" } ] }, { "day_name": "Пятниця", "classes": [ { "number": 3, "name": "(Лекція) Операційні сист та технолог їх захисту: Гулак Н.К.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/deb-rcae-bwm" }, { "number": 4, "name": "(Лекція) Управління інформаційною безпекою: Казмірчук С.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/jjy-vxyo-nsa" } ] } ] } ] }, { "group_number": 2, "weeks": [ { "week_number": 1, "week_days": [ { "day_name": "Понеділок1", "classes": [ { "number": 2, "name": "(Лабораторна) Управління інформаційною безпекою: Коломієць М.В.", "shouldBeVisited": false, "meetLink": "https://meet.google.com/uat-bmtm-msk" }, { "number": 3, "name": "(Лабораторна) Захищені компютерні сист та  мережі: Кривокульська О.О.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 4, "name": "(Лабораторна) Операційні сист та технолог їх захисту:  Панівко В.І.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/kmb-kkbn-vpk" }, { "number": 5, "name": "(Практична) Організаційне забезпечення захисту ін.: Телющенко В.А.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/xfq-pzav-vse" } ] }, { "day_name": "Вівторок", "classes": [ { "number": 3, "name": "(Лекція) Прикладна криптологія: Ільєнко А.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/nsh-htkt-zdj" }, { "number": 4, "name": "(Лекція) Захищені компютерні сист та  мережі: Єлізаров А.Б.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/xud-mqci-ovg" }, { "number": 5, "name": "(Лабораторна) Прикладна криптологія: Прокопенко О.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/rtd-unck-zbj" }, { "number": 6, "name": "(Лабораторна) Прикладна криптологія: Прокопенко О.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/rtd-unck-zbj" } ] }, { "day_name": "Середа", "classes": [] }, { "day_name": "Четвер", "classes": [ { "number": 4, "name": "(Лекція) Організаційне забезпечення захисту ін.: Петренко А.Б.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 5, "name": "(Лекція) Ліцензування та сертифік у сф зах інф: Хорошко В.О.", "shouldBeVisited": false, "meetLink": "-" } ] }, { "day_name": "Пятниця", "classes": [ { "number": 3, "name": "(Лекція) Управління інформаційною безпекою: Казмірчук С.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/jjy-vxyo-nsa" }, { "number": 4, "name": "(Лекція) Операційні сист та технолог їх захисту: Гулак Н.К.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/deb-rcae-bwm" } ] } ] }, { "week_number": 2, "week_days": [ { "day_name": "Понеділок2", "classes": [ { "number": 1, "name": "(Лабораторна) Ліцензування та сертифік у сф зах інф: Хохлачева Ю.Є.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 2, "name": "(Лабораторна) Ліцензування та сертифік у сф зах інф: Хохлачева Ю.Є.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 3, "name": "(Лабораторна) Авіаційна безп та кібербез авіац інф сис: Іванченко І.С.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/vhr-ucpf-pwq" }, { "number": 4, "name": "(Лабораторна) Авіаційна безп та кібербез авіац інф сис: Іванченко І.С.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/vhr-ucpf-pwq" } ] }, { "day_name": "Вівторок", "classes": [ { "number": 3, "name": "(Лекція) Прикладна криптологія: Ільєнко А.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/nsh-htkt-zdj" }, { "number": 4, "name": "(Лекція) Захищені компютерні сист та  мережі: Єлізаров А.Б.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/xud-mqci-ovg" } ] }, { "day_name": "Середа", "classes": [] }, { "day_name": "Четвер", "classes": [ { "number": 4, "name": "(Лекція) Організаційне забезпечення захисту ін.: Петренко А.Б.", "shouldBeVisited": false, "meetLink": "-" }, { "number": 5, "name": "(Лекція) Авіаційна безп та кібербез авіац інф сис: Іванченко Є.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/vhr-ucpf-pwq" } ] }, { "day_name": "Пятниця", "classes": [ { "number": 3, "name": "(Лекція) Операційні сист та технолог їх захисту: Гулак Н.К.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/deb-rcae-bwm" }, { "number": 4, "name": "(Лекція) Управління інформаційною безпекою: Казмірчук С.В.", "shouldBeVisited": true, "meetLink": "https://meet.google.com/jjy-vxyo-nsa" } ] } ] } ] } ] }'
    data = json.loads(json_string)
    groups = data['groups']
    for group in groups:
        group_num = group['group_number']
        if group_num != search_group:
            continue
        weeks = group['weeks']
        schedule_arr['weeks'] = weeks
    return schedule_arr['weeks']


class Class:
    number: int
    name: str
    should_be_visited: bool
    meet_link: str

    def __str__(self):
        should_be_visited = 'можна прогулять'
        if self.should_be_visited:
            should_be_visited = 'нада сходить'
        return str(
            self.number) + ') ' + self.getTime()[
                   1] + ' \n    ' + self.name + ' \n    ' + should_be_visited + ' \n    ' + self.meet_link

    def __repr__(self):
        should_be_visited = 'можна прогулять'
        if self.should_be_visited:
            should_be_visited = 'нада сходить'
        return str(self.number) + ') ' + self.name + ' ' + should_be_visited

    def __init__(self, number: int, name: str, should_be_visited: bool, meet_link: str) -> None:
        self.number = number
        self.name = name
        self.should_be_visited = should_be_visited
        self.meet_link = meet_link

    def getNumber(self):
        return self.number

    def getName(self):
        return self.name

    def getShould_be_visited(self):
        return self.should_be_visited

    def getMeet_link(self):
        return self.meet_link

    def getTime(self):
        beginings = [['07:55', '08:00'], ['09:45', '09:50'], ['11:35', '11:40'], ['13:25', '13:30'], ['15:15', '15:20'],
                     ['17:05', '17:10'], ['18:55', '19:00']]
        return beginings[self.number - 1]


class WeekDay:
    day_name: str
    classes: List[Class]

    def __str__(self):
        return self.day_name

    def __repr__(self):
        return self.day_name

    def __init__(self, day_name, classes) -> None:
        self.day_name = day_name
        self.classes = []
        for clas in classes:
            self.classes.append(Class(clas['number'], clas['name'], clas['shouldBeVisited'], clas['meetLink']))

    def getName(self):
        return self.day_name

    def getClasses(self):
        return self.classes


class Week:
    week_number: int
    week_days: List[WeekDay]

    def __str__(self):
        return self.week_number

    def __repr__(self):
        return self.week_number

    def __init__(self, week_number, week_days) -> None:
        self.week_number = week_number
        self.week_days = []
        for day in week_days:
            self.week_days.append(WeekDay(day['day_name'], day['classes']))

    def getWeekNum(self):
        return self.week_number

    def getWeekDays(self):
        return self.week_days

    def getDayClassesByDayName(self, dayName="Понеділок"):
        try:
            classes = self.week_days[WeekDayResolver.getDayNumberByName(dayName)].classes
        except Exception:
            classes = []
        return classes


class MainResolver:
    weeks: List

    def __init__(self, weeks: List) -> None:
        self.weeks = []
        for week in weeks:
            self.weeks.append(Week(week['week_number'], week['week_days']))

    def getWeeks(self):
        return self.weeks

    def getWeekByNumber(self, number):
        searched_week = None
        for week in self.weeks:
            if week.getWeekNum() == number:
                searched_week = week
                break
        return searched_week


class WeekDayResolver:
    @staticmethod
    def getDayNumberByName(week_name):
        week_days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя']
        for index, week_day in enumerate(week_days):
            if week_day == week_name:
                day_number = index
        return day_number

    @staticmethod
    def getDayNameByNumber(week_number):
        week_days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя']
        return week_days[week_number]


def startWatching(message):

    try:
        print('startWatching started !!!!!!!')
        while is_watching:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            todays_date = date.today()
            week_num = get_week_num(todays_date.day, todays_date.month, todays_date.year)
            obj = MainResolver(getDecodedSchedule(number_group.selected_group))
            week = obj.getWeekByNumber(week_num)
            day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(todays_date.day % 7))
            for clas in day_classes:
                clas_time = str(clas.getTime()[0])
                if str(clas_time) == str(current_time) and now.strftime("%S") == '01':
                    bot.send_message(message.chat.id, str(clas),
                                     disable_notification=bool(not clas.should_be_visited))
                    time.sleep(1)
            if str(current_time) == '11:00' and todays_date.day % 7 != 5 and todays_date.day % 7 != 4 and now.strftime("%S") == '01':
                tomorrow_date = todays_date + timedelta(days=1)
                week_num = get_week_num(tomorrow_date.day, tomorrow_date.month, tomorrow_date.year)
                obj = MainResolver(getDecodedSchedule(number_group.selected_group))
                week = obj.getWeekByNumber(week_num)
                day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(tomorrow_date.day % 7))
                reply = 'Пари на завтра:\n'
                for clas in day_classes:
                    reply += str(clas) + '\n'
                if reply == 'Пари на завтра:\n':
                    reply = 'завтра нема пар'
                bot.send_message(message.chat.id, reply, disable_web_page_preview=True)
                time.sleep(1)
            time.sleep(1)
    except Exception as e:
        print(e)
        msg = bot.send_message(message.chat.id, "🎆Упс...Моніторинг сьогодні не працює :(🎆\nВиберіть іншу дію:")
        bot.register_next_step_handler(msg, process_schedule_step_1)


class UserData:
    selected_group: int
    selected_week: int
    selected_day: str

    def __init__(self, selected_group):
        self.selected_group = selected_group
        self.selected_week = 1
        self.selected_day = 'Понеділок'

    def __str__(self):
        return 'группа: ' + str(self.selected_group) + ';\nтиждень: ' + str(
            self.selected_week) + ';\nдень: ' + self.selected_day + ';'


def get_week_num(day: int, month: int, year: int) -> int:
    calendar_ = calendar.TextCalendar(calendar.MONDAY)
    lines = calendar_.formatmonth(year, month).split('\n')
    days_by_week = [week.lstrip().split() for week in lines[2:]]
    str_day = str(day)
    week_num = 1
    for index, week in enumerate(days_by_week):
        if str_day in week:
            if (index + 1) % 2 == 0:
                week_num = 2
            return week_num


@bot.message_handler(commands=['start'])
def start_message(message):
    empty_markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id,
                           "Привіт ✌️, я бот-помічник. Введіть номер своєї підгрупи (1/2):",
                           reply_markup=empty_markup)
    bot.register_next_step_handler(msg, process_group_step)


def process_group_step(message):
    try:
        if message.text == '1' or message.text == '2':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Переглянути розклад", "Запустити Моніторинг")
            markup.add("Назад👈")
            msg = bot.send_message(message.chat.id,
                                   f'Відстежується <u style="color:000000">{message.text} підгрупа</u>, виберіть наступну дію:',
                                   reply_markup=markup, parse_mode="html")
            # переходимо на гілку підгрупи
            user_data = UserData(int(message.text))
            user_dict[message.chat.id] = user_data
            global number_group
            number_group = user_data
            bot.register_next_step_handler(msg, process_schedule_step_1)
        else:
            msg = bot.reply_to(message, 'Невірний номер підгрупи! Введіть ще раз:')
            bot.register_next_step_handler(msg, process_group_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Щось пішло не так :(')


def menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Сьогодні', 'Завтра')
    markup.add('Обрати за днем тижня')
    markup.add("Назад👈", "Зміна підгрупи♻")
    return markup


def process_schedule_step_1(message):
    try:
        if message.text == 'Переглянути розклад':
            msg = bot.send_message(message.chat.id, 'Виберіть один із запропонованих варіантів:', reply_markup=menu())
            bot.register_next_step_handler(msg, process_schedule_step_2)
        elif message.text == 'Запустити Моніторинг':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('/stop_monitoring')
            bot.send_message(message.chat.id, 'Моніторю розклад. Тепер бот буде надсилати сповіщення про пари😉',
                             reply_markup=markup)
            global is_watching
            is_watching = True
            startWatching(message)
        elif message.text == 'Назад👈':
            empty_markup = types.ReplyKeyboardRemove()
            msg = bot.send_message(message.chat.id, 'Введіть номер своєї підгрупи (1/2):', reply_markup=empty_markup)
            bot.register_next_step_handler(msg, process_group_step)
        else:
            msg = bot.send_message(message.chat.id, 'Невірний вибір! Спробуйте ще раз:')
            bot.register_next_step_handler(msg, process_schedule_step_1)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Щось пішло не так :(1')

@bot.message_handler(commands=['stop_monitoring'])
def process_stop_watching_schedule(message):
    try:
        global is_watching
        is_watching = False
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Переглянути розклад", "Запустити Моніторинг")
        markup.add("Назад👈")
        msg = bot.send_message(message.chat.id,
                               'Закінчив моніторити, виберіть наступну дію:',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_schedule_step_1)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Щось пішло не так :(stop_monitoring')


def process_schedule_step_2(message):
    try:
        if message.text == 'Сьогодні':
            bot.send_message(message.chat.id, 'Розклад на сьогодні')
            todays_date = date.today()
            week_num = get_week_num(todays_date.day, todays_date.month, todays_date.year)
            user_data = user_dict[message.chat.id]  # група
            obj = MainResolver(getDecodedSchedule(user_data.selected_group))
            week = obj.getWeekByNumber(week_num)
            day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(todays_date.day % 7))
            reply = ''
            for clas in day_classes:
                reply += str(clas) + '\n'
            msg = bot.send_message(message.chat.id, reply)
            bot.register_next_step_handler(msg, process_schedule_step_2)

        elif message.text == 'Завтра':
            bot.send_message(message.chat.id, 'Розклад на завтра')
            todays_date = date.today()
            tomorrow_date = todays_date + timedelta(days=1)
            week_num = get_week_num(tomorrow_date.day, tomorrow_date.month, tomorrow_date.year)
            user_data = user_dict[message.chat.id]  # група
            obj = MainResolver(getDecodedSchedule(user_data.selected_group))
            week = obj.getWeekByNumber(week_num)
            day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(tomorrow_date.day % 7))
            if not day_classes:
                msg = bot.send_message(message.chat.id, 'Пар немає. Виберіть один із запропонованих варіантів:')
                bot.register_next_step_handler(msg, process_schedule_step_2)
            else:
                reply = ''
                for clas in day_classes:
                    reply += str(clas) + '\n'
                msg = bot.send_message(message.chat.id, reply)
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

        elif message.text == "Назад👈":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Переглянути розклад", "Запустити Моніторинг")
            markup.add("Назад👈")
            msg = bot.send_message(message.chat.id, 'Виберіть наступну дію:',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, process_schedule_step_1)
        elif message.text == 'Зміна підгрупи♻':
            empty_markup = types.ReplyKeyboardRemove()
            msg = bot.send_message(message.chat.id, 'Введіть номер своєї підгрупи (1/2):',
                                   reply_markup=empty_markup)
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
        msg = bot.reply_to(message, 'Вихідний!!! Що будемо робити далі?')
        bot.register_next_step_handler(msg, process_schedule_step_2)


def process_schedule_step_3(message):
    try:
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
        bot.reply_to(message, 'Щось пішло не так :(3')


def process_schedule_step_4(message):
    try:
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
                bot.send_message(message.chat.id, reply)
                msg = bot.send_message(message.chat.id, 'Оберіть день:')
                bot.register_next_step_handler(msg, process_schedule_step_4)
        else:
            msg = bot.send_message(message.chat.id, 'Невірний вибір! Оберіть день:')
            bot.register_next_step_handler(msg, process_schedule_step_4)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Щось пішло не так :(4')


if __name__ == "__main__":
    bot.infinity_polling()
