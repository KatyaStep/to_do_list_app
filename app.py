import sys

from PyQt5.QtWidgets import QApplication

from controllers.main_controller import MainWindowController
from views.main_view import MainWindowView
from model.main_model import Model


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.app = QApplication(sys_argv)
        self.model = Model()
        self.controller = MainWindowController(self.model)
        self.main_view = MainWindowView(self.controller)

        self.controller.on_start_up()

        self.main_view.show()

        self.app.aboutToQuit.connect(self.closeEvent)

    def closeEvent(self):
        print("hello exit")
        self.model.clean()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
