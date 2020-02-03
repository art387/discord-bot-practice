from datetime import datetime
from todoist.api import TodoistAPI


class todoist_app:

    def __init__(self, token):
        self.api = TodoistAPI(token)
        self.api.sync()

    def getAllProject(self):
        return self.api.state['projects']

    def getAllTask(self):
        tasks_all = []
        items = self.api.state['items']
        for item in items:
            # d_task[item['id']] = item['content']
            tasks_all.append(item)
        return tasks_all

    def getTodayTask(self):
        tasks_today = []

        # Get "today", only keep Day XX Mon, which Todoist uses
        today = datetime.today().strftime("%Y-%m-%d")
        for item in self.api['items']:
            due = item['due']['date']
            if due:
                # Slicing :10 gives us the relevant parts
                if due[:10] == today or item['day_order'] <= 0:
                    tasks_today.append(item)

        return tasks_today

    def getFutureTask(self):
        tasks_future = []

        # Get "today", only keep Day XX Mon, which Todoist uses
        today = datetime.today().strftime("%Y-%m-%d")
        for item in self.api['items']:
            due = item['due']['date']
            if due:
                # Slicing :10 gives us the relevant parts
                if due[:10] == today or item['day_order'] > 0:
                    tasks_future.append(item)

        return tasks_future






