"""This module contains the functionality related to the ui for Main window"""

import logging

from PyQt5.QtCore import  QTimer
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from qtconsole.qtconsoleapp import QtCore
import views.edit_window


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

        self.disable_edit_menu()

        self.task_list.itemClicked.connect(self.item_click)
        self.edit_btn.clicked.connect(self.click_edit_btn)
        self.delete_btn.clicked.connect(self.click_delete_btn)
        self.add_task_qline.returnPressed.connect(self.get_task_text)
        self.complete_main_checkbox.clicked.connect(self.complete_task)
        self.incomplete_btn.clicked.connect(self.show_incomplete_tasks)
        self.completed_btn.clicked.connect(self.show_complete_tasks)

    def disable_edit_menu(self):
        """Disables the edit menu"""

        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        self.edit_btn.setStyleSheet(
            "border-radius: 6px; border : 2px solid grey; background-color: #dbe8f6; color: "
            "rgb(171, 171, 171); font: 12pt 'Chalkduster';"
        )
        self.delete_btn.setStyleSheet(
            "border-radius: 6px; border : 2px solid grey; background-color: #dbe8f6; color: "
            "rgb(171, 171, 171); font: 12pt 'Chalkduster';"
        )

        self.complete_main_checkbox.setEnabled(False)
        self.complete_main_checkbox.setStyleSheet(
            "color: rgb(171, 171, 171); font: 12pt 'Chalkduster';"
        )

    def enable_edit_menu(self):
        """Enables the edit menu"""

        self.edit_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

        self.edit_btn.setStyleSheet(
            "color: black; border-radius: 6px; border : 2px solid grey; background-color: "
            "#dbe8f6; font: 12pt 'Chalkduster';"
        )
        self.delete_btn.setStyleSheet(
            "color: black; border-radius: 6px; border : 2px solid grey; background-color: "
            "#dbe8f6; font: 12pt 'Chalkduster';"
        )

        self.complete_main_checkbox.setEnabled(True)
        self.complete_main_checkbox.setStyleSheet(
            "color: black; font: 12pt 'Chalkduster';"
        )

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

    def update_completed_task_number(self, num_tasks):
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

        for i in range(self.task_list.count()):
            if self.task_list.item(i) != item:
                self.task_list.item(i).setCheckState(QtCore.Qt.Unchecked)
                self.complete_main_checkbox.setCheckState(QtCore.Qt.Unchecked)

        if item.checkState():
            item.setCheckState(QtCore.Qt.Unchecked)
            self.disable_edit_menu()

        else:
            item.setCheckState(QtCore.Qt.Checked)
            self.enable_edit_menu()

        self.selected_item_name = item.text()

    def click_edit_btn(self):
        """Calls edit menu after edit button was clicked"""

        logging.debug("edit btn was clicked!!!!")
        edit_window = views.edit_window.EditWindow(self.controller, self.test_mode)
        task_id = self.task_list.currentRow() + 1  # because in db row_id starts with 1
        logging.debug(f'Selected item name: {self.selected_item_name}')

        self.controller.show_edit_window(
            self.test_mode, edit_window, task_id, self.selected_item_name
        )

    def click_delete_btn(self):
        """Calls controller function to delete the selected task"""
        task_id = (
            self.task_list.currentRow() + 1
        )
        self.confirm_delete_task(task_id, self.selected_item_name)

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

            msg.setInformativeText("Are you sure you want to delete this item?")
            msg.setWindowTitle("Message")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            return_val = msg.exec_()

            if return_val == QMessageBox.Ok:
                confirm_delete = True

        if confirm_delete:
            self.controller.delete_task(task_id, task_name)
            item_idx = task_id - 1
            self.task_list.takeItem(item_idx)
        else:
            logging.debug("Cancel was clicked")

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

        logging.debug("We are in update-task-name")
        list_task_id = task_id - 1
        self.task_list.item(list_task_id).setText(task_name)

    def complete_task(self):
        """Complete the task"""
        if self.complete_main_checkbox.checkState():
            task_id = self.task_list.currentRow() + 1
            task_name = self.selected_item_name
            self.controller.complete_task(task_id, task_name)

            if self.test_mode:
                self.remove_task_from_list()
            else:
                QTimer.singleShot(1000, self.remove_task_from_list)

            logging.debug("Trying to complete this task")
        else:
            logging.debug("Task is not gonna be complete")

    def remove_task_from_list(self):
        """Remove task from the list after completion"""
        self.task_list.takeItem(self.task_list.currentRow())
        self.complete_main_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.controller.update_task_overview()

    def show_incomplete_tasks(self):
        """Shows all incomplete tasks on the main page"""

        self.set_default_completed_btn()

        if self.incomplete_btn.isChecked():
            self.controller.get_incomplete_task()
            self.incomplete_btn.setStyleSheet(
                "font: 13pt 'Chalkduster'; color: black; background-color: #dbe8f6;"
                "border: 1px solid grey; border-width: 1px; border-radius: 10px;"
                )
        else:
            self.set_default_incomplete_btn()
            self.clear_task_list()
            self.controller.update_task_list()

    def show_complete_tasks(self):
        """Shows all incomplete tasks on the main page"""

        self.set_default_incomplete_btn()

        if self.completed_btn.isChecked():
            logging.debug('Complete btn was clicked')
            self.controller.get_completed_task()
            self.completed_btn.setStyleSheet(
                "font: 13pt 'Chalkduster'; color: black; background-color: #dbe8f6;"
                "border: 1px solid grey; border-width: 1px; border-radius: 10px;"
                )
        else:
            self.set_default_completed_btn()
            self.clear_task_list()
            self.controller.update_task_list()

    def clear_task_list(self):
        """Clear the task view list"""

        self.task_list.clear()

    def set_default_incomplete_btn(self):
        """Set to the default state Incomplete btn"""

        self.incomplete_btn.setChecked(False)
        self.incomplete_btn.setStyleSheet(
            "font: 13pt 'Chalkduster'; color: black; background-color: white;"
            "border: 1px solid grey; border-width: 1px; border-radius: 10px;"
        )

    def set_default_completed_btn(self):
        """Set to the default state Completed btn"""

        self.completed_btn.setChecked(False)
        self.completed_btn.setStyleSheet(
            "font: 13pt 'Chalkduster'; color: black; background-color: white;"
            "border: 1px solid grey; border-width: 1px; border-radius: 10px;"
        )
