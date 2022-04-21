"""This module contains the functionality related to the db queries and task data."""

import logging
import sqlite3
from collections import namedtuple


def get_db_connection():
    """Connect to the db"""
    return sqlite3.connect("/Users/katestepanova/repos/to_do_list_app/data/data.db")


Task = namedtuple('Task', 'task_id name due_date completed notes removed')


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
            task = Task(*result)
            tasks.append(task)

        return tasks

    def create_task(self, task_name):
        """Insert a new task into db

        Parameters
        ----------
        task_name: str
            the name of a new task
        """

        query = (
            "INSERT INTO tasks(name, due_date, completed, notes, removed) VALUES (?, ?, ?, ?, ?)"
        )
        not_completed = 0
        not_removed = 0
        row = (task_name, "never", not_completed, "NULL", not_removed)

        self.cursor.execute(query, row)
        self.app_db.commit()

    def get_last_added_task(self):
        """Gets last added task from db"""

        query = "SELECT rowid, * FROM tasks ORDER BY rowid ASC;"
        results = self.cursor.execute(query).fetchall()[-1]

        return Task(*results)

    def get_task_info(self, task) -> Task:
        """Get a task info from db for edit window launch

         Parameters
        ----------
        task_id - int
            id of a task that equals rowid in db
        """
        task_id, task_name = task

        query_select = "SELECT rowid, * FROM tasks WHERE rowid=?;"
        valid_result = self.cursor.execute(query_select, (task_id,)).fetchone()

        db_task_id = valid_result[0]
        db_task_name = valid_result[1]

        if valid_result is not None:
            if db_task_id != task_id or db_task_name != task_name:
                query = "SELECT rowid, *  FROM tasks WHERE name=?;"
                result = self.cursor.execute(query, (task_name,)).fetchone()
            else:
                result = valid_result
        else:
            query = "SELECT rowid, *  FROM tasks WHERE name=?;"
            result = self.cursor.execute(query, (task_name,)).fetchone()

        return Task(*result)

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

        logging.debug(f'This is previous name {previous_name}')
        logging.debug(f'This is task_id name {task_id}')

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

        logging.debug(f'This task is gonna be deleted: {task_name}')

        select_query = "SELECT rowid, name FROM tasks WHERE rowid=?"
        results = self.cursor.execute(select_query, (task_id,)).fetchone()
        removed = 1

        if results is not None:
            rowid = results[0]
            name = results[1]
            if (rowid == task_id) and (name == task_name):
                query = "UPDATE  tasks SET removed=? WHERE rowid=?"
                self.cursor.execute(query, (removed, task_id,))
                self.app_db.commit()
                return True

        query = "UPDATE  tasks SET removed=? WHERE name=?"
        self.cursor.execute(query, (removed, task_name,))
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

        logging.debug(f'This task is gonna be completed: {task_name}')

        select_query = "SELECT rowid, name FROM tasks WHERE rowid=?"
        results = self.cursor.execute(select_query, (task_id,)).fetchone()
        completed = 1

        if results is not None:
            rowid = results[0]
            name = results[1]
            if (rowid == task_id) and (name == task_name):
                query = "UPDATE tasks SET completed = ? WHERE rowid=?"
                self.cursor.execute(
                    query,
                    (
                        completed,
                        task_id,
                    ),
                )
                self.app_db.commit()
                return True

        query = "UPDATE tasks SET completed = ? WHERE name=?"
        self.cursor.execute(
            query,
            (
                completed,
                task_name,
            ),
        )
        self.app_db.commit()

        return True

    def get_completed_tasks(self):
        """Gets the list of all COMPLETED tasks from db"""

        tasks = []
        query = "SELECT rowid, * FROM tasks WHERE completed = ? AND removed = ? ORDER BY rowid ASC"
        completed = 1
        not_removed = 0
        results = self.cursor.execute(query, (completed, not_removed,)).fetchall()
        for result in results:
            task = Task(*result)
            tasks.append(task)

        return tasks

    def get_incomplete_tasks(self):
        """Gets the list of  incomplete tasks from db"""

        incomplete_tasks = []

        query = "SELECT name FROM tasks WHERE completed = ? AND removed = ? ORDER BY rowid ASC"
        not_completed = 0
        not_removed = 0

        results = self.cursor.execute(query, (not_completed, not_removed,)).fetchall()
        for name in results:
            incomplete_tasks.append(name[0])

        return incomplete_tasks
