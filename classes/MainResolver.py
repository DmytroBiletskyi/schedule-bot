import logging
from typing import List
from datetime import datetime, timedelta, date
from helpers.helpers import get_week_num


class Class:
    number: int
    lesson_type: str
    teacher_name: str
    name: str
    should_be_visited: bool
    meet_link: str
    class_link: str

    def __str__(self):
        return str(self.number) + ') ' + self.getTime()[1] + '-' + self.getTime()[2] +' (' + self.lesson_type + ')' + ' \n    ' + self.name + self.getShould_be_visited() + ' \n    ' + self.teacher_name + self.meet_link + self.class_link

    def __repr__(self):
        return str(self.number) + ') ' + self.name + ' ' + self.getShould_be_visited(),

    def __init__(self, number: int, name: str, should_be_visited: bool, meet_link: str, lesson_type: str, teacher_name: str, class_link: str) -> None:
        self.number = number
        self.name = name
        self.should_be_visited = should_be_visited
        self.meet_link = meet_link
        self.lesson_type = lesson_type
        self.teacher_name = teacher_name
        self.class_link = class_link

    def getNumber(self):
        return self.number

    def getName(self):
        return self.name

    def getShould_be_visited(self):
        return ''
        # return ' \n    ' + ("нада сходить" if self.should_be_visited else "можна прогулять")

    def getMeet_link(self):
        return ' \n    ' + "<a href='" + self.meet_link + "'>meet link</a>" if self.meet_link else ""

    def getClass_link(self):
        return ' \n    ' + "<a href='" + self.class_link + "'>class link</a>" if self.class_link else ""

    def getTime(self):
        beginings = [['07:55', '08:00', '09:35'], ['09:45', '09:50', '11:25'], ['11:35', '11:40', '13:15'], ['13:25', '13:30', '15:05'], ['15:15', '15:20', '16:55'],
                     ['17:05', '17:10', '18:45'], ['18:55', '19:00', '20:35']]
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
            self.classes.append(Class(clas['number'], clas['name'], clas['shouldBeVisited'], clas['meetLink'], clas['type'], clas['teacher_name'], clas['class_link']))

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

    def getNextClass(self, week_num=None, day_name=None):
        try:
            now = datetime.strptime(datetime.now().strftime('%H:%M') ,'%H:%M')
            today_date = date.today()
            if day_name is not None and week_num is not None:
                week = self.getWeekByNumber(week_num)
                day_classes = week.getDayClassesByDayName(day_name)
            else:
                week_num = get_week_num(today_date.day, today_date.month, today_date.year)
                week = self.getWeekByNumber(week_num)
                day_classes = week.getDayClassesByDayName(WeekDayResolver.getDayNameByNumber(today_date.weekday()))
            next_class = next((x for x in day_classes if datetime.strptime(x.getTime()[1] ,'%H:%M') > now), None)

            return {"object": next_class, "time_left": str(datetime.strptime(next_class.getTime()[1], '%H:%M') - now)}
        except Exception as e:
            logging.error('func: getNextClass || error: ' + str(e))


class WeekDayResolver:
    @staticmethod
    def getDayNumberByName(week_name):
        day_number = 1
        week_days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя']
        for index, week_day in enumerate(week_days):
            if week_day == week_name:
                day_number = index
        return day_number

    @staticmethod
    def getDayNameByNumber(week_number):
        week_days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя']
        return week_days[week_number]