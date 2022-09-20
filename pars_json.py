import json

with open("static/schedule.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    week = data['weeks'][0]
    for i in week['week_days']:
        print(i['day_name'])