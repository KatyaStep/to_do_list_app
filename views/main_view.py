from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QDialog
from PyQt5.uic import loadUi
from qtconsole.qtconsoleapp import QtCore


class EditWindow(QDialog):
    def __init__(self, controller):
        super(EditWindow, self).__init__()
        self.controller = controller
        self.controller.set_edit_window(self)
        self.edit_ui = "views/edit_window.ui"
        loadUi(self.edit_ui, self)

    def show_window(self):
        self.controller.show_edit_window()


class MainWindowView(QMainWindow, QDialog):
    def __init__(self, controller):
        super(MainWindowView, self).__init__()
        self.controller = controller
        self.controller.set_view(self)
        self.ui = "views/mainwindow.ui"
        loadUi(self.ui, self)

        # self.controller.get_task_list()
        # self.controller.get_num_all_tasks()
        self.disable_edit_menu()

        self.edit_btn.clicked.connect(self.click_edit_btn)
        self.add_task_qline.returnPressed.connect(self.get_task_text)
        self.task_list.itemClicked.connect(self.item_click)

    def disable_edit_menu(self):
        self.edit_btn.setEnabled(False)
        self.edit_btn.setStyleSheet("border-radius: 6px; border : 2px solid grey; background-color: #dbe8f6; color: "
                                    "rgb(171, 171, 171);")
        self.complete_main_checkbox.setEnabled(False)
        self.complete_main_checkbox.setStyleSheet("color: rgb(171, 171, 171)")

    def enable_edit_menu(self):
        self.edit_btn.setEnabled(True)
        self.edit_btn.setStyleSheet("color: black; border-radius: 6px; border : 2px solid grey; background-color: "
                                    "#dbe8f6;")

        self.complete_main_checkbox.setEnabled(True)
        self.complete_main_checkbox.setStyleSheet("color: black;")

    def add_task(self, task_name):
        item = QListWidgetItem(task_name)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.task_list.addItem(item)

    def update_task_count(self, num_tasks):
        self.tasks_num.setText(num_tasks)

    def update_overdue_task_count(self, num_tasks):
        self.overdue_num.setText(num_tasks)

    def update_completed_task_update(self, num_tasks):
        self.completed_num.setText(num_tasks)

    def get_task_text(self):
        text = self.add_task_qline.text()
        self.controller.add_task_to_the_list(text)
        self.add_task_qline.clear()

    def item_click(self, item):
        print(f'{item.text()} was clicked!!!!')
        if item.checkState():
            item.setCheckState(QtCore.Qt.Unchecked)
            self.disable_edit_menu()
        else:
            item.setCheckState(QtCore.Qt.Checked)
            self.enable_edit_menu()

        # edit_window = EditWindow(self.controller)
        # edit_window.show_window()

    def click_edit_btn(self):
        print('edit btn was clicked!!!!')
        edit_window = EditWindow(self.controller)
        edit_window.show_window()

