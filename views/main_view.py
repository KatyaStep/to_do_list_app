from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QDialog
from PyQt5.uic import loadUi
from qtconsole.qtconsoleapp import QtCore
from datetime import date, timedelta


class EditWindow(QDialog):
    def __init__(self, controller):
        super(EditWindow, self).__init__()
        self.controller = controller
        self.controller.set_edit_window(self)
        self.edit_ui = "views/edit_window.ui"
        loadUi(self.edit_ui, self)

        self.edit_task_name_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.notes_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.save_changes_btn.clicked.connect(self.get_changes)
        self.due_date_box.activated.connect(self.due_date_select)
        # self.due_date_list_options()

    def due_date_list_options(self, due_date):
        # self.due_date_box.clear()
        current_date = date.today()
        due_date_options = {
            0: due_date,
            1: f'Today: {current_date.strftime("%b/%d")}',
            2: f'Tomorrow: {(current_date + timedelta(days=1)).strftime("%b/%d")}',
            3: 'No due date',
            4: 'Calendar'
        }
        for index, item in due_date_options.items():
            self.due_date_box.insertItem(index, item)

        self.calendarWidget.hide()

    def due_date_select(self):
        # curr_due_date = self.due_date_box.itemText(0)
        idx = self.due_date_box.currentIndex()
        if idx == 4:
            self.calendarWidget.show()
        else:
            self.calendarWidget.hide()

        print(self.due_date_box.currentText())

    def task_info(self, task):
        self.edit_task_name_lineEdit.setText(task.name)
        self.due_date_list_options(task.due_date)
        # self.due_date_box.setCurrentText(task.due_date)
        self.notes_lineEdit.setText(task.notes)
        # self.edit_completed_checkBox.setCheckState(QtCore.Qt.Unchecked)

    def get_changes(self):
        task_name = self.edit_task_name_lineEdit.text()
        due_date = self.due_lineEdit.text()
        completed = self.edit_completed_checkBox.checkState()
        notes = self.notes_lineEdit.text()

        print(task_name, due_date, completed, notes)
        self.controller.save_changes(task_name, due_date, completed, notes)


class MainWindowView(QMainWindow):
    """
    A class used to represent Main window

    Attributes
    ----------
    controller: object
        instance of class MainWindowController(QObject)

    Methods
    -------
    disable_edit_menu(self)
    enable_edit_menu(self)
    add_task(self, task_name)
    update_task_count(self, num_tasks)
    update_overdue_task_count(self, num_tasks)
    update_completed_task_update(self, num_tasks)
    get_task_text(self)
    item_click(self, item)
    click_edit_btn(self)

    """
    def __init__(self, controller):
        """
        Parameters
        ----------
        controller :object
            instance of class MainWindowController(QObject)
        """

        super(MainWindowView, self).__init__()
        self.controller = controller
        self.controller.set_view(self)
        self.ui = "views/mainwindow.ui"
        loadUi(self.ui, self)

        # self.controller.get_task_list()
        # self.controller.get_num_all_tasks()
        self.disable_edit_menu()

        self.task_list.itemClicked.connect(self.item_click)
        self.edit_btn.clicked.connect(self.click_edit_btn)
        self.add_task_qline.returnPressed.connect(self.get_task_text)


    def disable_edit_menu(self):
        """Disable the edit menu"""

        self.edit_btn.setEnabled(False)
        self.edit_btn.setStyleSheet("border-radius: 6px; border : 2px solid grey; background-color: #dbe8f6; color: "
                                    "rgb(171, 171, 171); font: 12pt 'Chalkduster';")
        self.complete_main_checkbox.setEnabled(False)
        self.complete_main_checkbox.setStyleSheet("color: rgb(171, 171, 171); font: 12pt 'Chalkduster';")

    def enable_edit_menu(self):
        """Enable the edit menu"""

        self.edit_btn.setEnabled(True)
        self.edit_btn.setStyleSheet("color: black; border-radius: 6px; border : 2px solid grey; background-color: "
                                    "#dbe8f6; font: 12pt 'Chalkduster';")

        self.complete_main_checkbox.setEnabled(True)
        self.complete_main_checkbox.setStyleSheet("color: black; font: 12pt 'Chalkduster';")

    def add_task(self, task_name):
        """Add a new task to the task_list widget

        Parameters
        ----------
        task_name: str
            The name of the task
        """

        item = QListWidgetItem(task_name)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.task_list.addItem(item)

    def update_task_count(self, num_tasks):
        """Update the total amount of tasks that a user has

        Parameters
        ----------
        num_tasks: str
            Total amount of tasks that a user has
        """

        self.tasks_num.setText(num_tasks)

    def update_overdue_task_count(self, num_tasks):
        """Update the total amount of tasks that are overdue

        Parameters
        ----------
        num_tasks: str
            Total amount of tasks that are overdue
        """

        self.overdue_num.setText(num_tasks)

    def update_completed_task_update(self, num_tasks):
        """Update the total amount of tasks that are completed

        Parameters
        ----------
        num_tasks: str
            Total amount of tasks that are completed
        """

        self.completed_num.setText(num_tasks)

    def get_task_text(self):
        """Get a task text after user typed it in the field "Add a task". Call a controller to add the task
         to the list. Clean the field"""

        text = self.add_task_qline.text()
        self.controller.add_task_to_the_list(text)
        self.add_task_qline.clear()

    def item_click(self, item):
        """Disable or Enable the edit menu after item(a task) was clicked on

        Parameters
        ----------
        item: class 'PyQt5.QtWidgets.QListWidgetItem'
            The task in the task_list that was clicked.
        """
        self.task_name = item.text()
        print(self.task_name)
        # print(f'{item.text()} was clicked!!!!')
        if item.checkState():
            item.setCheckState(QtCore.Qt.Unchecked)
            self.disable_edit_menu()
        else:
            item.setCheckState(QtCore.Qt.Checked)
            self.enable_edit_menu()

        # edit_window = EditWindow(self.controller)
        # edit_window.show_window()

        # print(self.task_list.currentRow())

    def click_edit_btn(self):
        """Call edit menu after edit button was clicked"""

        print('edit btn was clicked!!!!')
        edit_window = EditWindow(self.controller)
        task_id = self.task_list.currentRow() + 1  # because in db row_id starts with 1
        print(task_id)
        self.controller.show_edit_window(edit_window, task_id)

