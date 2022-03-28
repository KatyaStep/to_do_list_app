import sqlite3


def get_db_connection():
    return sqlite3.connect('/Users/katestepanova/repos/to_do_list_app/data/data.db')


class Task:
    def __init__(self, name, due_date, completed):
        self.name = name
        self.due_date = due_date
        self.completed = completed


class Model:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor()

        # self.get_all_tasks_from_db()

    def clean(self):
        self.db.close()

    def __del__(self):
        if self.db:
            self.clean()

    def get_all_tasks(self):
        tasks = []
        query = "SELECT * FROM tasks"
        results = self.cursor.execute(query).fetchall()
        for result in results:
            name = str(result[0])
            due_date = str(result[1])
            completed = str(result[2])
            tasks.append(Task(name, due_date, completed))

        return tasks

    def create_task(self, new_task):
        query = "INSERT INTO tasks(name, due_date, completed) VALUES (?, ?, ?)"
        row = (new_task, 'never',  'False')

        self.cursor.execute(query, row)
        self.db.commit()

    def get_last_added_task(self):
        tasks = []
        query = 'SELECT * FROM tasks'
        results = self.cursor.execute(query).fetchall()[-1]

        name = str(results[0])
        due_date = str(results[1])
        completed = str(results[2])

        tasks.append(Task(name, due_date, completed))

        return tasks