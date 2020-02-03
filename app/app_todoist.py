from datetime import datetime
from todoist.api import TodoistAPI
import database_config as cfg


class todoist_app:

    def getAllProject(self):
        api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
        api.sync()
        return api.state['projects']

    def getAllTask(self):
        tasks_all = []
        api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
        api.sync()
        items = api.state['items']
        for item in items:
            # d_task[item['id']] = item['content']
            tasks_all.append(item)
        return tasks_all

    def getTodayTask(self):
        tasks_today = []
        api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
        api.sync()

        # Get "today", only keep Day XX Mon, which Todoist uses
        today = datetime.today().strftime("%Y-%m-%d")
        for item in api['items']:
            due = item['due']['date']
            if due:
                # Slicing :10 gives us the relevant parts
                if due[:10] == today or item['day_order'] <= 0:
                    tasks_today.append(item)

        return tasks_today

    def getFutureTask(self):
        tasks_future = []
        api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
        api.sync()

        # Get "today", only keep Day XX Mon, which Todoist uses
        today = datetime.today().strftime("%Y-%m-%d")
        for item in api['items']:
            due = item['due']['date']
            if due:
                # Slicing :10 gives us the relevant parts
                if due[:10] == today or item['day_order'] > 0:
                    tasks_future.append(item)

        return tasks_future






