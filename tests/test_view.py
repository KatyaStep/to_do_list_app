"""This module contains tests """

from datetime import date

from qtconsole.qtconsoleapp import QtCore

from mock_model import MockModel
from views.main_view import MainWindowView, EditWindow
from controllers.main_controller import MainWindowController


def test_add_new_task(qtbot, name):
    """This test checks the adding a new task to the list functionality

     Parameters
    ----------
    qtbot:
        test utility for simulating interaction with PyQt widgets
    name:
        command line argument that indicates test mode for the app
    """

    data = []

    model = MockModel(data)
    # model = Model()
    controller = MainWindowController(model)
    window = MainWindowView(controller, name)
    # window.show()
    qtbot.addWidget(window)

    # qtbot.mouseClick(window.edit_btn, QtCore.Qt.LeftButton)
    qtbot.keyClicks(window.add_task_qline, "Kate_test_task")
    qtbot.keyPress(window.add_task_qline, QtCore.Qt.Key_Enter)

    # assert name == True
    assert window.task_list.count() == 1
    assert window.task_list.item(0).text() == "Kate_test_task"

    # assert window.add_task_qline.text() == 'test_task'
    # assert window.edit_btn.text() == 'Edit'
    # assert window.windowTitle() == 'To Do App'


def test_delete_task(qtbot, name):
    """This test checks the delete a new task from the list functionality
     Parameters

    ----------
    qtbot:
        test utility for simulating interaction with PyQt widgets
    name:
        command line argument that indicates test mode for the app
    """

    data = []

    model = MockModel(data)
    controller = MainWindowController(model)
    window = MainWindowView(controller, name)
    # window.show()
    qtbot.addWidget(window)

    # qtbot.mouseClick(window.edit_btn, QtCore.Qt.LeftButton)
    qtbot.keyClicks(window.add_task_qline, "Kate_test_task_2")
    qtbot.keyPress(window.add_task_qline, QtCore.Qt.Key_Enter)

    rect = window.task_list.visualItemRect(window.task_list.item(0))
    center = rect.center()
    # window.task_list.item(0).setFocus()
    qtbot.mouseClick(window.task_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    qtbot.mouseClick(window.delete_btn, QtCore.Qt.LeftButton)

    assert window.task_list.count() == 0
    # assert False


def test_edit_task(qtbot, name):
    """This test checks the editing functionality: edit the name, due date and notes in the Edit window

     Parameters
    ----------
    qtbot:
        test utility for simulating interaction with PyQt widgets
    name:
        command line argument that indicates test mode for the app
    """

    data = []
    model = MockModel(data)
    controller = MainWindowController(model)
    window = MainWindowView(controller, name)
    edit_window = EditWindow(controller, name)
    # window.show()
    # assert window.isVisible()

    qtbot.addWidget(window)
    qtbot.keyClicks(window.add_task_qline, "Kate_test_task_3")
    qtbot.keyPress(window.add_task_qline, QtCore.Qt.Key_Enter)

    rect = window.task_list.visualItemRect(window.task_list.item(0))
    center = rect.center()
    # window.task_list.item(0).setFocus()
    qtbot.mouseClick(window.task_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    qtbot.mouseClick(window.edit_btn, QtCore.Qt.LeftButton)
    # edit_window.show()
    # print("Here is should be the name of the task: ", edit_window.edit_task_name_lineEdit.text())
    # assert edit_window.isVisible()
    qtbot.addWidget(edit_window)

    # print("Here is should be the name of the task: ", edit_window.edit_task_name_lineEdit.text())
    # assert False

    # Edit task name
    qtbot.keyClicks(edit_window.edit_task_name_lineEdit, "Kate_test_task_4")
    edit_window.notes_lineEdit.clear()
    # Edit note field
    qtbot.keyClicks(edit_window.notes_lineEdit, "A note for Kate_test_task_4")

    # Edit due date
    current_date = date.today()
    edit_window.due_date_box.insertItem(0, current_date.strftime("%b/%d"))
    edit_window.due_date_box.setCurrentIndex(0)
    assert edit_window.due_date_box.currentText() == current_date.strftime("%b/%d")

    qtbot.mouseClick(edit_window.save_changes_btn, QtCore.Qt.LeftButton)
    # print('What is a text for due date: ', edit_window.due_date_box.currentText())

    # Check that name was edited on the main screen
    assert window.task_list.item(0).text() == "Kate_test_task_4"

    # qtbot.mouseClick(edit_window.due_date_box.view(), QtCore.Qt.LeftButton )
    # edit_window.due_date_box.setCurrentIndex(1)
    #
    # print('What is a text for due date: ', edit_window.due_date_box.currentText())
    # qtbot.mouseClick(edit_window.save_changes_btn, QtCore.Qt.LeftButton)

    # Open edited task one more time and check that note was edited
    qtbot.mouseClick(window.task_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    qtbot.mouseClick(window.edit_btn, QtCore.Qt.LeftButton)
    assert edit_window.notes_lineEdit.text() == "A note for Kate_test_task_4"

    # print('This is edit task note: ', edit_window.notes_lineEdit.text())
    #
    # for item in data:
    #     print(item)

    # assert False

    # assert edit_window.notes_lineEdit.text() == 'A note for Kate_test_task_4'


def test_complete_task(qtbot, name):
    """This test checks that tasks can be checked as completed

     Parameters
    ----------
    qtbot:
        test utility for simulating interaction with PyQt widgets
    name:
        command line argument that indicates test mode for the app
    """

    data = []
    model = MockModel(data)
    controller = MainWindowController(model)
    window = MainWindowView(controller, name)
    # window.show()
    # assert window.isVisible()

    qtbot.addWidget(window)
    qtbot.keyClicks(window.add_task_qline, "Kate_test_task_5")
    qtbot.keyPress(window.add_task_qline, QtCore.Qt.Key_Enter)

    rect = window.task_list.visualItemRect(window.task_list.item(0))
    center = rect.center()
    # window.task_list.item(0).setFocus()
    qtbot.mouseClick(window.task_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    qtbot.mouseClick(window.complete_main_checkbox, QtCore.Qt.LeftButton)

    assert window.task_list.count() == 0
    assert int(window.completed_num.text()) == 1


def test_ui_main_window(qtbot, name):
    """This test checks the ui of the Main window

     Parameters
    ----------
    qtbot:
        test utility for simulating interaction with PyQt widgets
    name:
        command line argument that indicates test mode for the app
    """

    data = []
    model = MockModel(data)
    controller = MainWindowController(model)
    window = MainWindowView(controller, name)
    # window.show()
    # assert window.isVisible()

    qtbot.addWidget(window)

    assert window.windowTitle() == "To Do App"
    assert window.edit_btn.text() == "Edit"
    assert window.delete_btn.text() == "Delete"
    assert window.complete_main_checkbox.text() == "Complete"
    assert window.imcomplete_btn.text() == "Incomplete"
    assert window.completed_btn.text() == "Completed"

    # qtbot.mouseClick(window.left_panel_menu.viewport(),QtCore.Qt.LeftButton)
    assert window.menu_header.text() == "Inbox"
    assert window.left_panel_menu.item(0).text() == "All Tasks"
    assert window.left_panel_menu.item(1).text() == "Today"
    assert window.left_panel_menu.item(2).text() == "Tomorrow"
    assert window.left_panel_menu.item(3).text() == "This Week"
    assert window.left_panel_menu.item(4).text() == "Trash"

    assert window.all_tasks_lbl.text() == "All Tasks"
    assert window.tasks_label.text() == "tasks"
    assert window.overdue_label.text() == "overdue"
    assert window.completed_label.text() == "completed"


def test_ui_edit_window(qtbot, name):
    """This test checks the ui of the Edit window

     Parameters
    ----------
    qtbot:
        test utility for simulating interaction with PyQt widgets
    name:
        command line argument that indicates test mode for the app
    """

    data = []
    model = MockModel(data)
    controller = MainWindowController(model)
    window = MainWindowView(controller, name)
    edit_window = EditWindow(controller, name)
    # window.show()
    # assert window.isVisible()

    qtbot.addWidget(window)
    qtbot.keyClicks(window.add_task_qline, "Kate_test_task_3")
    qtbot.keyPress(window.add_task_qline, QtCore.Qt.Key_Enter)

    rect = window.task_list.visualItemRect(window.task_list.item(0))
    center = rect.center()
    # window.task_list.item(0).setFocus()
    qtbot.mouseClick(window.task_list.viewport(), QtCore.Qt.LeftButton, pos=center)
    qtbot.mouseClick(window.edit_btn, QtCore.Qt.LeftButton)
    # edit_window.show()
    # print("Here is should be the name of the task: ", edit_window.edit_task_name_lineEdit.text())
    # assert edit_window.isVisible()
    # qtbot.addWidget(edit_window)

    # assert False
    assert edit_window.windowTitle() == "Edit"
    assert edit_window.summary_lbl.text() == "Summary"
    assert edit_window.due_date_lbl.text() == "due"
    assert edit_window.tags_lbl.text() == "tags"
    assert edit_window.note_lbl.text() == "Notes"

    # assert edit_window.edit_task_name_lineEdit.text() == 'Kate_test_task_3'
