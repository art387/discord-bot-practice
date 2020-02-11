from datetime import datetime

from discord.ext.commands import bot
from todoist.api import TodoistAPI
from discord.ext import tasks, commands

import database_config as cfg
from tabulate import tabulate


class Todoist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_tasks = None
        self.current_ctx = None
        self.current_command = 'today'

        try:
            self.api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
            self.api.sync()
            self.scheduler_todo_today.start()
        except Exception as e:
            print(e)

    def table_print(self, tasks_list, current_command=None):
        if not current_command:
            current_command = self.current_command
        if not tasks_list:
            return "No Schedule"
        table = list()
        for i, task in enumerate(tasks_list):
            table.append([i + 1, task['content']])
        response = (tabulate(table, headers=["No", "Task"]))
        return "Here is your uncompleted schedule for {}, <@{}>!".format(current_command,
                                                                         cfg.YOUR_DISCORD_USER_ID) + '\n' + response

    @tasks.loop(minutes=30)
    async def scheduler_todo_today(self):
        await self.bot.wait_until_ready()
        tasks_list = self.get_today_task()
        if tasks_list:
            ch = self.bot.get_channel(cfg.YOUR_DISCORD_CHANNEL)
            response = self.table_print(tasks_list, 'today')
            await ch.send(response)

    @commands.command()
    async def todo(self, ctx, arg1, arg2=None):
        # use double " to pass a string argument
        response = ""
        if arg1 == 'today' or arg1 == 'future' or arg1 == 'all':
            self.current_ctx = ctx
            tasks_list = []
            if arg1 == 'today':
                tasks_list = self.get_today_task()
            elif arg1 == 'future':
                tasks_list = self.get_future_task()
            elif arg1 == 'all':
                tasks_list = self.get_all_task()
            response = self.table_print(tasks_list)
        elif arg1 == 'do':
            response = self.set_task_complete(arg2)
        elif arg1 == 'project':
            self.get_all_project()
            response = 'boo'
        # elif arg1 == 'add':
        #     await ctx.send(self.add_item(arg2))
        else:
            response = 'Boo, wrong command!'

        try:
            await ctx.send(response)
        except Exception as e:
            print(e)

    # TODO: Fix the add item on todoist API
    def add_item(self, argument):
        try:
            item = self.api.items.add(argument)
            self.api.commit()
            self.api.sync()
            return "Add item success"
        except Exception as e:
            print(e)
            return "Commit failed"

    def get_all_project(self):
        return self.api.state['projects']

    def get_all_task(self):
        try:
            tasks_all = []
            items = self.api.state['items']
            for item in items:
                # d_task[item['id']] = item['content']
                tasks_all.append(item)
            self.current_tasks = tasks_all
            self.current_command = 'all'
            return tasks_all
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"

    def get_today_task(self):
        try:
            self.api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
            self.api.sync()
            tasks_today_uncompleted = []
            # Get "today", only keep Day XX Mon, which Todoist uses
            today = datetime.today().strftime("%Y-%m-%d")
            for item in self.api.state['items']:
                # due = item[]['due']['date']
                due = item.data['due']['date']
                if due:
                    # Slicing :10 gives us the relevant parts
                    if due[:10] <= today and item.data['checked'] == 0:
                        tasks_today_uncompleted.append(item)
            self.current_tasks = tasks_today_uncompleted
            self.current_command = 'today'
            return tasks_today_uncompleted
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"

    def get_future_task(self):
        try:
            self.api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
            self.api.sync()
            tasks_future = []
            today = datetime.today().strftime("%Y-%m-%d")
            for item in self.api.state['items']:
                due = item['due']['date']
                if due:
                    # Slicing :10 gives us the relevant parts
                    if due[:10] > today and item.data['checked'] == 0:
                        tasks_future.append(item)
            self.current_tasks = tasks_future
            self.current_command = 'future'
            return tasks_future
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"

    def set_task_complete(self, id_content):
        try:

            self.api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
            self.api.sync()

            for curr_id in id_content.split():
                task = self.current_tasks[int(curr_id) - 1]
                task_id = task.data["id"]
                item = self.api.items.get_by_id(task_id)
                item.close()
            self.api.commit()

            tasks_list = []
            if self.current_command == 'today':
                tasks_list = self.get_today_task()
            elif self.current_command == 'future':
                tasks_list = self.get_future_task()
            elif self.current_command == 'all':
                tasks_list = self.get_all_task()
            response = self.table_print(tasks_list)

            return 'Commit Success' + '\n' + response

        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"


def setup(bot):
    bot.add_cog(Todoist(bot))
