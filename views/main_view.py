"""This module contains the functionality related to the ui for Edit and Main windows"""

from datetime import date, timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QDialog, QMessageBox
from PyQt5.uic import loadUi
from qtconsole.qtconsoleapp import QtCore


# class ConfirmDialogSave(QDialog):
#     """
#     A class used to represent Confirmation dialog-window.
#
#     Attributes
#     ----------
#     controller: object
#         instance of class MainWindowController(QObject)
#
#     Methods
#     -------
#     close_window(self)
#
#     """
#
#     def __init__(self, controller):
#         super().__init__()
#         self.controller = controller
#         self.controller.set_confirmation_dialog(self)
#         self.confirm_dialog = "views/confirmation_save_dialog.ui"
#         loadUi(self.confirm_dialog, self)
#
#         self.message_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
#         self.ok_btn.clicked.connect(self.close_window)
#
#     def close_window(self):
#         """Closes the Confirmation-dialog window"""
#         self.close()


class EditWindow(QDialog):
    """
    A class used to represent Edit window

    Attributes
    ----------
    controller: object
        instance of class MainWindowController(QObject)

    Methods
    -------
    due_date_list_options(self, due_date)
    due_date_select(self)
    task_info(self, task)
    get_changes(self)
    """

    def __init__(self, controller, mode):
        super().__init__()
        self.controller = controller
        self.controller.set_edit_window(self)
        self.test_mode = mode
        self.edit_ui = "views/edit_window.ui"
        self.confirm_dialog = None
        # self.confirm_dialog = "views/confirmation_save_dialog.ui"
        # loadUi(self.confirm_dialog, self)
        loadUi(self.edit_ui, self)

        self.edit_task_name_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.notes_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.due_date_box.activated.connect(self.due_date_select)
        self.calendarWidget.selectionChanged.connect(self.pick_calendar_date)
        self.save_changes_btn.clicked.connect(self.save_changes)
        # self.due_date_list_options()

    def due_date_list_options(self, due_date):
        """Show a list of due_date options in a dropdown list.

        Parameters
        ----------
        due_date: str
            The due_date for the selected task
        """

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
        """Select new due_date. If option is "Calendar" then show a calendar."""

        # curr_due_date = self.due_date_box.itemText(0)
        idx = self.due_date_box.currentIndex()
        if idx == 4:
            # self.calendarWidget.setSelectedDate(self.due_date_box.itemText(0))
            self.calendarWidget.show()
        else:
            self.calendarWidget.hide()

        print(self.due_date_box.currentText())

    def pick_calendar_date(self):
        """Pick a new date from a calendar."""
        date_selected = self.calendarWidget.selectedDate().toPyDate()
        print(f"Date selected: {date_selected}")

        # self.due_date_box.setCurrentIndex(5)
        self.due_date_box.setItemText(0, str(date_selected))
        self.due_date_box.setCurrentIndex(0)

        # print(self.due_date_box.currentText())

    def task_info(self, task):
        """
        Show a task info: name, due_date, notes, tags in Edit mode

        Parameters
        ----------
        task: object
            The instance of class Task (located in main_model.py file)
        """

        self.edit_task_name_lineEdit.setText(task.name)
        self.due_date_list_options(task.due_date)
        # self.due_date_box.setCurrentText(task.due_date)
        self.notes_lineEdit.setText(task.notes)
        # self.edit_completed_checkBox.setCheckState(QtCore.Qt.Unchecked)

    # def get_changes(self):
    #     """Get new variables for the task: name, due_date, completed, notes."""
    #
    #     task_name = self.edit_task_name_lineEdit.text()
    #     due_date = self.due_lineEdit.text()
    #     completed = self.edit_completed_checkBox.checkState()
    #     notes = self.notes_lineEdit.text()
    #
    #     print(task_name, due_date, completed, notes)
    #     self.controller.save_changes(task_name, due_date, completed, notes)

    def save_changes(self):
        """Save changes after editing a task. New variables: task_name, due_date, notes"""
        print("Save btn was clicked")
        task_name = self.edit_task_name_lineEdit.text()
        due_date = self.due_date_box.currentText()
        print("SAVE CHANGES:", due_date)
        notes = self.notes_lineEdit.text()

        # confirm_dialog = ConfirmDialogSave(self.controller)
        # self.controller.set_confirmation_dialog(confirm_dialog)
        self.controller.save_changes(task_name, due_date, notes)
        self.show_confirm_dialog()
        self.close()


    def show_confirm_dialog(self):
        """Create a confirmation message window to notify a user about successfully saved changes"""

        if not self.test_mode:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Congratulations")
            msg.setInformativeText("Your changes have been successfully saved!")
            msg.setWindowTitle("Message")
            # msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            # msg.buttonClicked.connect(msgbtn)

            retval = msg.exec_()
            print("value of pressed message box button:", retval)


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

    def __init__(self, controller, mode):
        """
        Parameters
        ----------
        controller :object
            instance of class MainWindowController(QObject)
        """

        super().__init__()
        self.controller = controller
        self.controller.set_view(self)
        self.test_mode = mode
        self.main_window_ui = "views/mainwindow.ui"
        loadUi(self.main_window_ui, self)

        self.selected_item_name = None
        # self.controller.get_task_list()
        # self.controller.get_num_all_tasks()
        self.disable_edit_menu()

        self.task_list.itemClicked.connect(self.item_click)
        self.edit_btn.clicked.connect(self.click_edit_btn)
        self.delete_btn.clicked.connect(self.click_delete_btn)
        self.add_task_qline.returnPressed.connect(self.get_task_text)

    def disable_edit_menu(self):
        """Disables the edit menu"""

        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        self.edit_btn.setStyleSheet("border-radius: 6px; border : 2px solid grey; background-color: #dbe8f6; color: "
                                    "rgb(171, 171, 171); font: 12pt 'Chalkduster';")
        self.delete_btn.setStyleSheet("border-radius: 6px; border : 2px solid grey; background-color: #dbe8f6; color: "
                                      "rgb(171, 171, 171); font: 12pt 'Chalkduster';")

        self.complete_main_checkbox.setEnabled(False)
        self.complete_main_checkbox.setStyleSheet("color: rgb(171, 171, 171); font: 12pt 'Chalkduster';")

    def enable_edit_menu(self):
        """Enables the edit menu"""

        self.edit_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

        self.edit_btn.setStyleSheet("color: black; border-radius: 6px; border : 2px solid grey; background-color: "
                                    "#dbe8f6; font: 12pt 'Chalkduster';")
        self.delete_btn.setStyleSheet("color: black; border-radius: 6px; border : 2px solid grey; background-color: "
                                      "#dbe8f6; font: 12pt 'Chalkduster';")

        self.complete_main_checkbox.setEnabled(True)
        self.complete_main_checkbox.setStyleSheet("color: black; font: 12pt 'Chalkduster';")

    def add_task(self, task_name):
        """Adds a new task to the task_list widget

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
        """Updates the total amount of tasks that a user has

        Parameters
        ----------
        num_tasks: str
            Total amount of tasks that a user has
        """

        self.tasks_num.setText(num_tasks)

    def update_overdue_task_count(self, num_tasks):
        """Updates the total amount of tasks that are overdue

        Parameters
        ----------
        num_tasks: str
            Total amount of tasks that are overdue
        """

        self.overdue_num.setText(num_tasks)

    def update_completed_task_update(self, num_tasks):
        """Updates the total amount of tasks that are completed

        Parameters
        ----------
        num_tasks: str
            Total amount of tasks that are completed
        """

        self.completed_num.setText(num_tasks)

    def get_task_text(self):
        """Gets a task text after user typed it in the field "Add a task". Calls a controller to add the task
         to the list. Cleans the field"""

        text = self.add_task_qline.text()
        self.controller.add_task_to_the_list(text)
        self.add_task_qline.clear()

    def item_click(self, item):
        """Disables or Enables the edit menu after item(a task) was clicked on

        Parameters
        ----------
        item: class 'PyQt5.QtWidgets.QListWidgetItem'
            The task in the task_list that was clicked.
        """
        # self.task_name = item.text()
        # print(self.task_name)
        # print(f'{item.text()} was clicked!!!!')
        for i in range(self.task_list.count()):
            if self.task_list.item(i) != item:
                self.task_list.item(i).setCheckState(QtCore.Qt.Unchecked)

        if item.checkState():
            item.setCheckState(QtCore.Qt.Unchecked)
            self.disable_edit_menu()

        else:
            item.setCheckState(QtCore.Qt.Checked)
            self.enable_edit_menu()

        self.selected_item_name = item.text()
        # edit_window = EditWindow(self.controller)
        # edit_window.show_window()

        # print(self.task_list.currentRow())

    def click_edit_btn(self):
        """Calls edit menu after edit button was clicked"""

        print('edit btn was clicked!!!!')
        edit_window = EditWindow(self.controller, self.test_mode)
        task_id = self.task_list.currentRow() + 1  # because in db row_id starts with 1
        print(self.selected_item_name)

        self.controller.show_edit_window(self.test_mode, edit_window, task_id, self.selected_item_name)

    def click_delete_btn(self):
        """Calls controller function to delete the selected task"""
        task_id = self.task_list.currentRow() + 1# # because in db row_id starts with 1
        # task_name = self.task_list.item(task_id).text()

        print(f"THIS IS TASK NAME: {self.selected_item_name}")

        self.confirm_delete_task(task_id, self.selected_item_name)
        # self.controller.delete_task(task_id)
        print("Delete btn clicked!!!")

    def confirm_delete_task(self, task_id, task_name):
        """Shows confirmation message for deleting the selected task

        Parameters
        ----------
        task_id: int
            id of a task that equals rowid in db (to make it equal to rowid you need to add 1)
        """
        confirm_delete = False

        if self.test_mode:
            confirm_delete = True
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)

            # msg.setText("Delete")
            msg.setInformativeText("Are you sure you want to delete this item?")
            msg.setWindowTitle("Message")
            # msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.buttonClicked.connect(self.delete_task)

            return_val = msg.exec_()

            if return_val == QMessageBox.Ok:
                confirm_delete = True

        if confirm_delete:
            self.controller.delete_task(task_id, task_name)
            item_idx = task_id - 1
            self.task_list.takeItem(item_idx)
        else:
            print("Cancel was clicked")

    def update_task_name(self, task_name, task_id):
        """Updates the name of the task in the list on the main window after editing

        Parameters
        ----------
        task_name: str
            new name of the task after editing
        task_id: int
            task id which equals rowid in db.
            To get the right id of the task in the widget_list you need to substitute 1 from task_id
        """

        print("We are in update-task-name")
        list_task_id = task_id - 1
        self.task_list.item(list_task_id).setText(task_name)
