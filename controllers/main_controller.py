"""This module contains functionality of a controller which communicates with view and model modules"""

from datetime import date
from PyQt5.QtCore import QObject


class MainWindowController(QObject):
    """
    A class used to represent Controlle module.

    Attributes
    ----------
    model: object
        instance of class Model

    Methods
    -------
    set_view(self, view)
    set_edit_window(self, edit_view)
    set_confirmation_dialog
    on_start_up(self)
    update_task_list
    update_task_overview
    add_task_to_the_list
    show_edit_window
    save_changes
    """

    def __init__(self, model):
        """
        Parameters
        ----------
        model :object
            instance of class Model
        """

        super().__init__()
        self.model = model
        self.tasks = self.model.get_all_tasks()
        self.edit_task_id = None
        self.view = None
        self.edit_view = None
        self.edit_task_name = None
        self.task = None
        # self.confirmation_view = None

    def set_view(self, view):
        """Initialize main_window(view module)

         Parameters
        ----------
        view: object
            instance of class MainWindowView(QMainWindow)
        """

        self.view = view

    def set_edit_window(self, edit_view):
        """Initialize edit window(view module)

        Parameters
        ----------
        edit_view: object
            instance of class EditWindow(QDialog)
        """

        self.edit_view = edit_view

    # def set_confirmation_dialog(self, confirm_dialog):
    #     """Initialize confirm dialog window(view module)
    #     Parameters
    #     ----------
    #     confirm_dialog: object
    #         instance of class ConfirmationDialog(QDialog)
    #     """
    #     self.confirmation_view = confirm_dialog

    def on_start_up(self):
        """Calls methods 'update_task_list(), update_task_overview() on the start of the app."""

        self.update_task_list()
        self.get_task_overview()

    def update_task_list(self):
        """Calling the view module to represent all task on the main page of the app"""

        for task in self.tasks:
            if task.completed == "False":
                self.view.add_task(task.name)

    def get_task_overview(self):
        """Updates tasks overview number on the main page of the app"""

        overdue_tasks = []
        completed_tasks = []

        curr_date = date.today()
        format_date = curr_date.strftime("%Y/%m/%d")

        for task in self.tasks:
            if task.due_date < format_date:
                overdue_tasks.append(task)
            if task.completed == "True":
                completed_tasks.append(task)
        #
        # for task in completed_tasks:
        #     print("This is completed task: ", task.name)

        self.view.update_task_count(str(len(self.tasks)))
        self.view.update_overdue_task_count(str(len(overdue_tasks)))
        self.view.update_completed_task_update(str(len(completed_tasks)))

    def add_task_to_the_list(self, task_name):
        """Adds a new task to the list on the main page of the app

        Parameters
        ----------
        task_name: str
            name of a new task
        """

        self.model.create_task(task_name)
        task = self.model.get_last_added_task()
        self.view.add_task(task.name)
        self.tasks = self.model.get_all_tasks()
        self.get_task_overview()

    def show_edit_window(self, test_mode, edit_window, task_id, task_name):
        """Launches edit window after pressing edit btn

        Parameters
        ----------
        edit_window: object
            instance of EditWindow(QDialog)
        task_id: int
            id of the task in the list which eguals rowid in db
        task_name:
        """

        # self.edit_task_name = task_name
        self.edit_task_id = task_id
        self.set_edit_window(edit_window)

        # task = self.model.get_task_info(self.edit_task_name)
        self.task = self.model.get_task_info(self.edit_task_id, task_name)
        # self.edit_view.task_info(task.id, task.name, task.due_date, task.completed, task.notes)
        self.edit_view.task_info(self.task)
        if not test_mode:
            self.edit_view.exec()
        # else:
        #     self.edit_view.show()

    def save_changes(self, task_name, due_date, notes):
        """Saves changes after editing a task

        Parameters
        ----------
        task_name: str
            edited task name
        due_date: str
            new due date
        notes: str
            notes for the task
        """
        data = {
            'previous_name': self.task.name,
            'edit_task_id': self.edit_task_id,
            'new_task_name': task_name,
            'due_date': due_date,
            'notes': notes,
        }
        self.model.update_task_info(data)
        # self.model.update_task_info(
        #     self.task.name, self.edit_task_id, task_name, due_date, notes
        # )
        self.view.update_task_name(task_name, self.edit_task_id)

    def delete_task(self, task_id, task_name):
        """Call model instance to delete a task from db

        Parameters
        ----------
        task_id: int
            task_id that equals rowid in db
        task_name: str
        """

        if self.model.delete_task(task_id, task_name):
            print("Deleted successfully")

    def complete_task(self, task_id, task_name):
        """Call model instance to change complete flag in db

        Parameters
        ----------
        task_id: int
            task_id that equals rowid in db
        task_name: str
        """

        self.model.complete_task(task_id, task_name)

    def update_task_overview(self):
        """Call model instance to update task overview number on the main screen of the app."""
        completed_tasks = self.model.get_completed_tasks()
        self.view.update_completed_task_update(str(len(completed_tasks)))
