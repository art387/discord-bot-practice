# from datetime import datetime
# from todoist.api import TodoistAPI
#
#
# class todoist_app:
#     def __init__(self, token, current_task):
#         self.api = TodoistAPI(token)
#         self.current_task = current_task
#         self.api.sync()
#
#     def resync_todoist(self):
#         self.api.sync()
#
#     def getAllProject(self):
#         return self.api.state['projects']
#
#     def getAllTask(self):
#         try:
#             tasks_all = []
#             items = self.api.state['items']
#             for item in items:
#                 # d_task[item['id']] = item['content']
#                 tasks_all.append(item)
#
#             self.current_task = tasks_all
#             return tasks_all
#         except:
#             return "Something wrong is happening, please check!"
#
#     def getTodayTask(self):
#         try:
#             tasks_today_uncompleted = []
#
#             # Get "today", only keep Day XX Mon, which Todoist uses
#             today = datetime.today().strftime("%Y-%m-%d")
#             for item in self.api.state['items']:
#                 # due = item[]['due']['date']
#                 due = item.data['due']['date']
#
#                 if due:
#                     # Slicing :10 gives us the relevant parts
#                     if due[:10] <= today and item.data['checked'] == 0:
#                         tasks_today_uncompleted.append(item)
#             self.current_task = tasks_today_uncompleted
#             return tasks_today_uncompleted
#         except Exception as e:
#             print(e)
#             return "Something wrong is happening, please check!"
#
#     def getFutureTask(self):
#         try:
#             tasks_future = []
#             # Get "today", only keep Day XX Mon, which Todoist uses
#             today = datetime.today().strftime("%Y-%m-%d")
#             for item in self.api.state['items']:
#                 due = item['due']['date']
#                 if due:
#                     # Slicing :10 gives us the relevant parts
#                     if due[:10] > today and item.data['checked'] == 0:
#                         tasks_future.append(item)
#             self.current_task = tasks_future
#             return tasks_future
#         except Exception as e:
#             print(e)
#             return "Something wrong is happening, please check!"
#
#     def setTaskComplete(self, id_content):
#         try:
#             task = self.current_task[int(id_content)-1]
#             id = task.data['id']
#             item = self.api.items.get_by_id(id)
#             item.close()
#             self.api.commit()
#             self.api.sync()
#             return "Commit Success"
#         except Exception as e:
#             print(e)
#             return "Something wrong is happening, please check!"
