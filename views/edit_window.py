"""This module contains the functionality related to the ui for Edit  window"""

from datetime import date, timedelta
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi


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

        loadUi(self.edit_ui, self)

        self.edit_task_name_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.notes_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.due_date_box.activated.connect(self.due_date_select)
        self.calendarWidget.selectionChanged.connect(self.pick_calendar_date)
        self.save_changes_btn.clicked.connect(self.save_changes)
        self.tagBox.activated.connect(self.tags_selection)
        # self.due_date_list_options()

    def due_date_list_options(self, due_date):
        """Show a list of due_date options in a dropdown list.

        Parameters
        ----------
        due_date: str
            The due_date for the selected task
        """

        current_date = date.today()
        due_date_options = {
            0: due_date,
            1: f'Today: {current_date.strftime("%b/%d")}',
            2: f'Tomorrow: {(current_date + timedelta(days=1)).strftime("%b/%d")}',
            3: "No due date",
            4: "Calendar",
        }
        for index, item in due_date_options.items():
            self.due_date_box.insertItem(index, item)

        self.calendarWidget.hide()

    def due_date_select(self):
        """Select new due_date. If option is "Calendar" then show a calendar."""

        idx = self.due_date_box.currentIndex()
        if idx == 4:
            self.calendarWidget.show()
        else:
            self.calendarWidget.hide()

        logging.debug(self.due_date_box.currentText())

    def pick_calendar_date(self):
        """Pick a new date from a calendar."""
        date_selected = self.calendarWidget.selectedDate().toPyDate()
        logging.debug(f"Date selected: {date_selected}")

        self.due_date_box.setItemText(0, str(date_selected))
        self.due_date_box.setCurrentIndex(0)

    def tags_list(self, current_tag):
        """Show a list of tags in a dropdown list.

        Parameters
        ----------
        current_tag: int
            The current tag index for the selected task
        """

        tags = self.controller.get_tags()

        for idx, tag in enumerate(tags):
            self.tagBox.insertItem(idx, tag)

        self.tagBox.setCurrentIndex(current_tag)

    def tags_selection(self):
        """Choose a new tag for the current task"""

        tag_idx = self.tagBox.currentIndex() + 1

        self.controller.change_tag(tag_idx)

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
        self.notes_lineEdit.setText(task.notes)
        self.tags_list(task.tag - 1)

    def save_changes(self):
        """Save changes after editing a task. New variables: task_name, due_date, notes"""
        logging.debug("Save btn was clicked")
        task_name = self.edit_task_name_lineEdit.text()
        due_date = self.due_date_box.currentText()
        notes = self.notes_lineEdit.text()

        logging.debug(f'Changes were saved:{task_name}, {due_date}, {notes}')
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
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()
