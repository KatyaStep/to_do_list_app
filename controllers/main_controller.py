from PyQt5.QtCore import QObject
from datetime import date


class MainWindowController(QObject):
    def __init__(self, model):
        super(MainWindowController, self).__init__()
        self.model = model
        self.tasks = self.model.get_all_tasks()

        self.edit_view = None
        self.edit_task_name = None

    def set_view(self, view):
        self.view = view

    def on_start_up(self):
        self.update_task_list()
        self.update_task_overview()

    def update_task_list(self):
        for task in self.tasks:
            self.view.add_task(task.name)

    def update_task_overview(self):
        overdue_tasks = []
        completed_tasks = []

        curr_date = date.today()
        format_date = curr_date.strftime("%Y/%m/%d")

        for task in self.tasks:
            if task.due_date < format_date:
                overdue_tasks.append(task)
            if task.completed == 'True':
                completed_tasks.append(task)

        self.view.update_task_count(str(len(self.tasks)))
        self.view.update_overdue_task_count(str(len(overdue_tasks)))
        self.view.update_completed_task_update(str(len(completed_tasks)))

    def add_task_to_the_list(self, task_name):
        self.model.create_task(task_name)
        task = self.model.get_last_added_task()
        self.view.add_task(task.name)
        self.tasks = self.model.get_all_tasks()
        self.update_task_overview()

    def set_edit_window(self, edit_view):
        self.edit_view = edit_view

    def show_edit_window(self, edit_window, task_id):
        # self.edit_task_name = task_name
        self.edit_task_id = task_id
        self.set_edit_window(edit_window)

        # task = self.model.get_task_info(self.edit_task_name)
        task = self.model.get_task_info(self.edit_task_id)
        # self.edit_view.task_info(task.id, task.name, task.due_date, task.completed, task.notes)
        self.edit_view.task_info(task)
        self.edit_view.exec()

    # def save_changes(self, task_name, due_date, completed, notes):
    #     self.model.update_task_info(task_name, due_date, completed, notes, self.edit_task_name)








# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindowController()
#     window.show()
#     sys.exit(app.exec())
