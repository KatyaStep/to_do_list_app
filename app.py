"""This module initializes the app"""

import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from controllers.main_controller import MainWindowController
from views.main_view import MainWindowView
from model.main_model import Model


class App(QApplication):
    """
    A class used to represent applicationa

    Attributes
    ----------
    sys_argv: command lines argument

    Methods
    -------
    close_event(self)
    """

    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        test_mode = False
        if sys_argv[1] == "--test_config":
            test_mode = True
        self.app = QApplication(sys_argv)
        self.model = Model()
        self.controller = MainWindowController(self.model)
        self.main_view = MainWindowView(self.controller, test_mode)

        self.controller.on_start_up()

        self.main_view.show()

        if sys_argv[1] == "--test_config":
            print(f"Got our argument from command line: {sys_argv[1]}")

        self.app.aboutToQuit.connect(self.close_event)

    def close_event(self):
        """Call the function clean from model.py"""
        print("hello exit")
        self.model.clean()


if __name__ == "__main__":
    app = App(sys.argv)
    app.setWindowIcon(QtGui.QIcon("app_icon.png"))
    sys.exit(app.exec())
