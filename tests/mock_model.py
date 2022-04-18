"""This module mocks the functionality related to the db queries and task data."""


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
        # self.app_db = get_db_connection()
        # self.cursor = self.app_db.cursor()

        # self.get_all_tasks_from_db()

    def clean(self):
        """Close the db connection"""

        # self.app_db.close()

    def __del__(self):
        """Calls self.clean method if db connection was established"""

        # if self.app_db:
        #     self.clean()

    def get_all_tasks(self):
        """Gets the list of all tasks from db"""

        tasks = []
        for task in self.data:
            temp_task_storage = {
                'task_id': task["row_id"],
                'name': str(task["name"]),
                'due_date': task["due_date"],
                'completed': str(task["completed"]),
                'notes': str(task["notes"]),
            }
            # row_id = task["row_id"]
            # name = str(task["name"])
            # due_date = task["due_date"]
            # completed = str(task["completed"])
            # notes = str(task["notes"])
            tasks.append(Task(temp_task_storage))
            # tasks.append(Task(row_id, name, due_date, completed, notes))

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
                "completed": False,
                "notes": None,
            }
        )

    def get_last_added_task(self):
        """Gets last added task from db"""

        # row_id = self.data[-1]["row_id"]
        # name = self.data[-1]["name"]
        # due_date = self.data[-1]["due_date"]
        # completed = self.data[-1]["completed"]
        # notes = self.data[-1]["notes"]

        temp_task_storage = {
            'task_id': self.data[-1]["row_id"],
            'name': self.data[-1]["name"],
            'due_date': self.data[-1]["due_date"],
            'completed': self.data[-1]["completed"],
            'notes': self.data[-1]["notes"],
        }
        # return Task(row_id, name, due_date, completed, notes)
        return Task(temp_task_storage)

    def get_task_info(self, task_id, task_name):
        """Get a task info from db for edit window launch

         Parameters
        ----------
        task_id - int
            id of a task that equals rowid in db
        """

        for _, task in enumerate(self.data):
            if task["row_id"] == task_id:
                # print(f"THIS IS TASK NAME FOR EDIT WINDOW: {task['name']}")
                temp_task_storage = {
                    'task_id': task_id,
                    'name':  task_name,
                    'due_date': task["due_date"],
                    'completed': task["completed"],
                    'notes': task["notes"],
                }
                # row_id = task["row_id"]
                # name = task["name"]
                # due_date = task["due_date"]
                # completed = task["completed"]
                # notes = task["notes"]
        return Task(temp_task_storage)
        # return Task(row_id, name, due_date, completed, notes)

    def update_task_info(self, updated_data):
        """Updates a task info in db

        Parameters
        ----------
        task_id - int
        new_name - str
        due_date - str
        notes - str
        """
        _, task_id, new_name, due_date, notes = updated_data.values()
        for _, task in enumerate(self.data):
            if task["row_id"] == task_id:
                task["name"] = new_name
                task["due_date"] = due_date
                task["notes"] = notes
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
                task["completed"] = "True"

    def get_completed_tasks(self):
        """Gets the list of all COMPLETED tasks from db"""
        tasks = []

        for idx, task in enumerate(self.data):
            if task["completed"] == "True":
                tasks.append(self.data[idx])

        return tasks
