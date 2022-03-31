import sqlite3

# from PyQt5.QtSql import QSqlQuery


def get_db_connection():
    return sqlite3.connect('/Users/katestepanova/repos/to_do_list_app/data/data.db')


class Task:
    def __init__(self, id_task, name, due_date, completed, notes):
        self.id = id_task
        self.name = name
        self.due_date = due_date
        self.completed = completed
        self.notes = notes


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
        query = "SELECT rowid, * FROM tasks"
        results = self.cursor.execute(query).fetchall()
        for result in results:
            id = result[0]
            name = str(result[1])
            due_date = str(result[2])
            completed = str(result[3])
            notes = str(result[4])
            tasks.append(Task(id, name, due_date, completed, notes))

        return tasks

    def create_task(self, task_name):
        query = "INSERT INTO tasks(name, due_date, completed, notes) VALUES (?, ?, ?, ?)"
        row = (task_name, 'never',  'False', 'NULL')

        self.cursor.execute(query, row)
        self.db.commit()

    def get_last_added_task(self):
        # tasks = []
        query = 'SELECT rowid, * FROM tasks ORDER BY rowid ASC'
        results = self.cursor.execute(query).fetchall()[-1]

        id = results[0]
        name = str(results[1])
        due_date = str(results[2])
        completed = str(results[3])
        notes = str(results[4])

        # tasks.append(Task(id, name, due_date, completed, notes))

        return Task(id, name, due_date, completed, notes)

    def get_task_info(self, task_id) -> Task:
        """Get a task info from db for edit window launch"""
        query = "SELECT rowid, * FROM tasks WHERE rowid=?;"
        # row = task_name
        # todo: make unique id and only return one task per query
        results = self.cursor.execute(query, (task_id,))
        for result in results:
            id = result[0]
            name = str(result[1])
            due_date = str(result[2])
            completed = str(result[3])
            notes = str(result[4])
        # todo return Task class instance
        return Task(id, name, due_date, completed, notes)

    def update_task_info(self, id, new_name, due_date, completed, notes):

        print("We are in update task info", new_name, due_date, completed, notes)
        query = "UPDATE tasks  SET name=?, due_date=?, completed=?, notes=? WHERE id=?"
        row = (new_name, due_date, completed, notes, id)
        self.cursor.execute(query, row)
        self.db.commit()
