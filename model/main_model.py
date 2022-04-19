"""This module contains the functionality related to the db queries and task data."""
import sqlite3


def get_db_connection():
    """Connect to the db"""
    return sqlite3.connect("/Users/katestepanova/repos/to_do_list_app/data/data.db")


class Task:
    """
    A class used to represent data of a task.

    Attributes
    ----------
    task_id: int
        task_id is a row_id in db
    name: str
        name of the task
    due_date: str
    completed: int (0 - False, 1-True)
    notes: str
    """

    def __init__(self, task):
        self.task_id = task['task_id']
        self.name = task['name']
        self.due_date = task['due_date']
        self.completed = task['completed']
        self.notes = task['notes']
        self.removed = task['removed']


class Model:
    """
     A class that gets/sends data from/into db.

    Methods
    -------
    clean(self)
    __del__(self)
    get_all_tasks(self)
    create_task(self, task_name)
    get_last_added_task(self)
    get_task_info(self, task_id)
    update_task_info(self, task_id, new_name, due_date, notes)

    """

    def __init__(self):
        self.app_db = get_db_connection()
        self.cursor = self.app_db.cursor()

        # self.get_all_tasks_from_db()

    def clean(self):
        """Close the db connection"""

        self.app_db.close()

    def __del__(self):
        """Calls self.clean method if db connection was established"""

        if self.app_db:
            self.clean()

    def get_all_tasks(self):
        """Gets the list of all tasks from db"""

        tasks = []
        query = "SELECT rowid, * FROM tasks ORDER BY rowid ASC"
        results = self.cursor.execute(query).fetchall()
        for result in results:
            # row_id = result[0]
            # name = str(result[1])
            # due_date = str(result[2])
            # completed = str(result[3])
            # notes = str(result[4])
            row_id, name, due_date, completed, notes, removed = result
            data = {
                'task_id': row_id,
                'name': name,
                'due_date': due_date,
                'completed': completed,
                'notes': notes,
                'removed': removed,
            }
            # tasks.append(Task(row_id, name, due_date, completed, notes))
            tasks.append(Task(data))

        return tasks

    def create_task(self, task_name):
        """Insert a new task into db

        Parameters
        ----------
        task_name: str
            the name of a new task
        """

        query = (
            "INSERT INTO tasks(name, due_date, completed, notes) VALUES (?, ?, ?, ?)"
        )
        row = (task_name, "never", "False", "NULL")

        self.cursor.execute(query, row)
        self.app_db.commit()

    def get_last_added_task(self):
        """Gets last added task from db"""

        # tasks = []
        query = "SELECT rowid, * FROM tasks ORDER BY rowid ASC;"
        results = self.cursor.execute(query).fetchall()[-1]

        row_id, name, due_date, completed, notes, removed = results
        data = {
            'task_id': row_id,
            'name': name,
            'due_date': due_date,
            'completed': completed,
            'notes': notes,
            'removed': removed,
        }
        # row_id = results[0]
        # name = str(results[1])
        # due_date = str(results[2])
        # completed = str(results[3])
        # notes = str(results[4])

        # tasks.append(Task(row_id, name, due_date, completed, notes))

        # return Task(row_id, name, due_date, completed, notes)

        return Task(data)

    def get_task_info(self, task_id, task_name) -> Task:
        """Get a task info from db for edit window launch

         Parameters
        ----------
        task_id - int
            id of a task that equals rowid in db
        """

        query_select = "SELECT rowid, * FROM tasks WHERE rowid=?;"
        # row = task_name
        # make unique row_id and only return one task per query
        valid_result = self.cursor.execute(query_select, (task_id,)).fetchone()
        # print("Here is valid result: ", task_id)
        if valid_result is not None:
            if valid_result[0] != task_id or valid_result[1] != task_name:
                query = "SELECT rowid, *  FROM tasks WHERE name=?;"
                result = self.cursor.execute(query, (task_name,)).fetchone()
            else:
                result = valid_result
        else:
            query = "SELECT rowid, *  FROM tasks WHERE name=?;"
            result = self.cursor.execute(query, (task_name,)).fetchone()

            # print("Task_id and task_name are NOT matched")
            # print(f'This is result: {results}')
            # for result in results:
            #     print(result)

        # print(result[0])
        # row_id = result[0]
        # name = str(result[1])
        # due_date = str(result[2])
        # completed = str(result[3])
        # notes = str(result[4])
        row_id, name, due_date, completed, notes, removed = result

        data = {
            'task_id': row_id,
            'name': name,
            'due_date': due_date,
            'completed': completed,
            'notes': notes,
            'removed': removed,
        }
        # return Task(row_id, name, due_date, completed, notes)
        return Task(data)

    # def update_task_info(self, previous_name, task_id, new_name, due_date, notes):
    def update_task_info(self, updated_data):
        """Updates a task info in db

        Parameters
        ----------
        task_id - int
        new_name - str
        due_date - str
        notes - str
        """

        previous_name, task_id, new_name, due_date, notes = updated_data.values()

        # print("We are in update task info", new_name, due_date, notes)
        print(f'This is previous name {previous_name}')
        print(f'This is task_id name {task_id}')
        select_query = "SELECT rowid, name FROM tasks WHERE rowid=?"
        results = self.cursor.execute(select_query, (task_id,)).fetchone()

        if results is not None:
            rowid = results[0]
            name = results[1]
            if (rowid == task_id) and (name == new_name):
                query = "UPDATE tasks  SET name=?, due_date=?, notes=? WHERE rowid=?"
                row = (new_name, due_date, notes, task_id)
                self.cursor.execute(query, row)
                self.app_db.commit()
                return

        query = "UPDATE tasks  SET name=?, due_date=?, notes=? WHERE name=?"
        row = (new_name, due_date, notes, previous_name)
        self.cursor.execute(query, row)
        self.app_db.commit()

    def delete_task(self, task):
        """Removes a task from db

        Parameters
        ----------
        task_id - int
        """
        task_id, task_name = task.values()
        print(f'DELETE  task: {task_name}')
        select_query = "SELECT rowid, name FROM tasks WHERE rowid=?"
        results = self.cursor.execute(select_query, (task_id,)).fetchone()
        # print("Task id: " , task_id)
        # print("Task name: ", task_name)
        # print(results)
        if results is not None:
            rowid = results[0]
            name = results[1]
            if (rowid == task_id) and (name == task_name):
                # query = "DELETE FROM tasks WHERE rowid=?"
                query = "UPDATE  tasks SET removed=? WHERE rowid=?"
                self.cursor.execute(query, (1, task_id,))
                self.app_db.commit()
                return True

        # query = "DELETE FROM tasks WHERE name=?"
        query = "UPDATE  tasks SET removed=? WHERE name=?"
        self.cursor.execute(query, (1, task_name,))
        self.app_db.commit()

        return True

    def complete_task(self, task):
        """Complete task changing the flag 'complete' in db"

        Parameters
        ----------
        task_id: int
        task_name: str
        """

        task_id, task_name = task.values()
        print(f'COMPLETE task: {task_name}')
        select_query = "SELECT rowid, name FROM tasks WHERE rowid=?"
        results = self.cursor.execute(select_query, (task_id,)).fetchone()
        # print("Task id: " , task_id)
        # print("Task name: ", task_name)
        # print(results)
        if results is not None:
            rowid = results[0]
            name = results[1]
            if (rowid == task_id) and (name == task_name):
                query = "UPDATE tasks SET completed = ? WHERE rowid=?"
                self.cursor.execute(
                    query,
                    (
                        1,
                        task_id,
                    ),
                )
                self.app_db.commit()
                return True

        query = "UPDATE tasks SET completed = ? WHERE name=?"
        self.cursor.execute(
            query,
            (
                1,
                task_name,
            ),
        )
        self.app_db.commit()

        return True

    def get_completed_tasks(self):
        """Gets the list of all COMPLETED tasks from db"""

        tasks = []
        query = "SELECT rowid, * FROM tasks WHERE completed = ? ORDER BY rowid ASC"
        results = self.cursor.execute(query, (1,)).fetchall()
        for result in results:
            # row_id = result[0]
            # name = str(result[1])
            # due_date = str(result[2])
            # completed = str(result[3])
            # notes = str(result[4])
            row_id, name, due_date, completed, notes, removed = result
            data = {
                'task_id': row_id,
                'name': name,
                'due_date': due_date,
                'completed': completed,
                'notes': notes,
                'removed':removed,
            }
            tasks.append(Task(data))
            # tasks.append(Task(row_id, name, due_date, completed, notes))

        return tasks
