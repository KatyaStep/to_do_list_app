"""This module initializes the app"""

import sys

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
        self.app = QApplication(sys_argv)
        self.model = Model()
        self.controller = MainWindowController(self.model)
        self.main_view = MainWindowView(self.controller)

        self.controller.on_start_up()

        self.main_view.show()

        self.app.aboutToQuit.connect(self.close_event)

    def close_event(self):
        """Call the function clean from model.py"""

        print("hello exit")
        self.model.clean()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
