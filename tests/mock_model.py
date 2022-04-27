"""This module mocks the functionality related to the db queries and task data."""

import logging
import datetime
from model.main_model import Task



class MockModel:
    """
    A class that used for test environment to mock getting/sending data to db.

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

    def __init__(self, data):
        self.data = data

    @staticmethod
    def clean():
        """Close the db connection"""
        logging.debug('The application was closed')
        # self.app_db.close()

    def __del__(self):
        """Calls self.clean method if db connection was established"""

        if self.data:
            self.clean()

    def get_all_tasks(self):
        """Gets the list of all tasks from db"""

        tasks = []
        for data in self.data:
            task = Task(*data)
            tasks.append(task)

        return tasks

    def create_task(self, task_name):
        """Insert a new task into db

        Parameters
        ----------
        task_name: str
            the name of a new task
        """

        last_row = len(self.data)
        self.data.append(
            {
                "row_id": last_row + 1,
                "name": task_name,
                "due_date": "04/30/22",
                "completed": 0,
                "notes": None,
                'removed': 0,
                'time_added': datetime.datetime.today().strftime("%m/%d/%y %H/%M/%S")
            }
        )

    def get_last_added_task(self):
        """Gets last added task from db"""
        task = self.data[-1].values()

        return Task(*task)


    def get_task_info(self, task_info):
        """Get a task info from db for edit window launch

         Parameters
        ----------
        task_id - int
            id of a task that equals rowid in db
        """
        task_id, _ = task_info

        for _, task in enumerate(self.data):
            if task["row_id"] == task_id:
                return Task(*(task.values()))

        return True

    def update_task_info(self, updated_data):
        """Updates a task info in db

        Parameters
        ----------
        task_id - int
        new_name - str
        due_date - str
        notes - str
        """
        task_id, new_name, due_date, notes, removed = updated_data.values()
        for _, task in enumerate(self.data):
            if task["row_id"] == task_id:
                task["name"] = new_name
                task["due_date"] = due_date
                task["notes"] = notes
                task['removed'] = removed
                # return True

    def delete_task(self, task_to_delete):
        """Removes a task from db

        Parameters
        ----------
        task_id - int
        """

        for idx, task in enumerate(self.data):
            if task["row_id"] == task_to_delete['task_id']:
                self.data.pop(idx)

    def complete_task(self, task_to_complete):
        """Complete task

        Parameters
        ----------
        task_id: int
        task_name: str

        """

        for _, task in enumerate(self.data):
            if task["row_id"] == task_to_complete['task_id']:
                task["completed"] = 1

    def get_completed_tasks(self):
        """Gets the list of all COMPLETED tasks from db"""
        tasks = []

        for idx, task in enumerate(self.data):
            if task["completed"] == 1:
                tasks.append(self.data[idx])

        return tasks
