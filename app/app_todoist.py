from datetime import datetime
from todoist.api import TodoistAPI
import requests

class todoist_app:

    def __init__(self, token, current_task):
        self.api = TodoistAPI(token)
        self.current_task = current_task
        self.api.sync()

        # uncomplete
        # item1 = self.api.items.get_by_id(3411314014)
        # item1.uncomplete()
        # item2 = self.api.items.get_by_id(3411331042)
        # item2.uncomplete()
        # self.api.commit()

    def resync_todoist(self):
        self.api.sync()

    def getAllProject(self):
        return self.api.state['projects']

    def getAllTask(self):
        tasks_all = []
        items = self.api.state['items']
        for item in items:
            # d_task[item['id']] = item['content']
            tasks_all.append(item)

        self.current_task = tasks_all
        return tasks_all

    def getTodayTask(self):
        tasks_today = []

        # Get "today", only keep Day XX Mon, which Todoist uses
        today = datetime.today().strftime("%Y-%m-%d")
        for item in self.api.state['items']:
            # due = item[]['due']['date']
            due = item.data['due']['date']

            if due:
                # Slicing :10 gives us the relevant parts
                if due[:10] <= today and item.data['checked'] == 0:
                    tasks_today.append(item)

        self.current_task = tasks_today
        return tasks_today

    def getFutureTask(self):
        tasks_future = []
        # Get "today", only keep Day XX Mon, which Todoist uses
        today = datetime.today().strftime("%Y-%m-%d")
        for item in self.api.state['items']:
            due = item['due']['date']
            if due:
                # Slicing :10 gives us the relevant parts
                if due[:10] > today and item.data['checked'] == 0:
                    tasks_future.append(item)
        self.current_task = tasks_future
        return tasks_future

    def setTaskComplete(self, id_content):
        try:
            task = self.current_task[int(id_content)]
            id = task.data['id']
            item = self.api.items.get_by_id(id)
            item.close()
            self.api.commit()
            self.api.sync()
            return "Commit Success"
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"
