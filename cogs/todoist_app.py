from datetime import datetime
from todoist.api import TodoistAPI
from discord.ext import tasks, commands

import database_config as cfg
from tabulate import tabulate


class Todoist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_task = []
        self.api = TodoistAPI(cfg.YOUR_TODOIST_TOKEN)
        self.api.sync()
        self.scheduler_todo_today.start()

    def resync_todoist(self):
        self.api.sync()

    @tasks.loop(minutes=30)
    async def scheduler_todo_today(self):
        await self.bot.wait_until_ready()
        table = list()
        tasks_list = self.get_today_task()
        if tasks_list:
            ch = self.bot.get_channel(cfg.YOUR_DISCORD_CHANNEL)
            for i, task in enumerate(tasks_list):
                table.append([i + 1, task['content']])
            print(tabulate(table, headers=["No", "Task"]))
            await ch.send('Here is your uncompleted schedule for today, <@%s>!' % cfg.YOUR_DISCORD_USER_ID +
                          '\n' + tabulate(table, headers=["No", "Task"]))

    @commands.command()
    async def todo(self, ctx, arg1, arg2=None):
        if arg1 == 'today' or arg1 == 'future' or arg1 == 'all':
            tasks_list = []
            if arg1 == 'today':
                tasks_list = self.get_today_task()
            elif arg1 == 'future':
                tasks_list = self.get_future_task()
            elif arg1 == 'all':
                tasks_list = self.get_all_task()
            if tasks_list != "Something wrong is happening, please check!":
                table = list()
                for i, task in enumerate(tasks_list):
                    table.append([i + 1, task['content']])
                print(tabulate(table, headers=["No", "Task"]))
                await ctx.send('Here is your uncompleted schedule for today, <@%s>!' % cfg.YOUR_DISCORD_USER_ID +
                               '\n' + tabulate(table, headers=["No", "Task"]))
            else:
                await ctx.send("Something wrong is happening, please check!")
        elif arg1 == 'do':
            response = self.set_task_complete(arg2)
            await ctx.send(response)
        elif arg1 == 'project':
            self.get_all_project()
        else:
            await ctx.send('Boo, wrong command!')

    def get_all_project(self):
        return self.api.state['projects']

    def get_all_task(self):
        try:
            tasks_all = []
            items = self.api.state['items']
            for item in items:
                # d_task[item['id']] = item['content']
                tasks_all.append(item)
            self.current_task = tasks_all
            return tasks_all
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"

    def get_today_task(self):
        try:
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
            self.current_task = tasks_today_uncompleted
            return tasks_today_uncompleted
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"

    def get_future_task(self):
        try:
            tasks_future = []
            today = datetime.today().strftime("%Y-%m-%d")
            for item in self.api.state['items']:
                due = item['due']['date']
                if due:
                    # Slicing :10 gives us the relevant parts
                    if due[:10] > today and item.data['checked'] == 0:
                        tasks_future.append(item)
            self.current_task = tasks_future
            return tasks_future
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"

    def set_task_complete(self, id_content):
        try:
            task = self.current_task[int(id_content) - 1]
            task_id = task.data["id"]
            item = self.api.items.get_by_id(task_id)
            item.close()
            self.api.commit()
            self.api.sync()
            return "Commit Success"
        except Exception as e:
            print(e)
            return "Something wrong is happening, please check!"


def setup(bot):
    bot.add_cog(Todoist(bot))
