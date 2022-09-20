class UserData:
    id: int
    selected_group: int
    selected_week: int
    selected_day: str
    is_watching: bool
    user_name: str
    activity_list: dict

    def __init__(self, id, selected_group, user_name):
        self.id = id
        self.selected_group = selected_group
        self.selected_week = 1
        self.selected_day = 'Понеділок'
        self.user_name = user_name
        self.is_watching = False
        self.activity_list = {}

    def __str__(self):
        return 'группа: ' + str(self.selected_group) + ';\nтиждень: ' + str(
            self.selected_week) + ';\nдень: ' + self.selected_day + ';'