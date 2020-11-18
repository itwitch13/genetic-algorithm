import sys
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from .AppView import AppWindowWidget
# from .GeneticAlgorithm import GeneticModel


log = logging.getLogger(__name__)


class LevyOptimalization(QtWidgets.QMainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("OE project")

        # View
        self.devWidget = AppWindowWidget()
        self.setCentralWidget(self.devWidget)

        # models
        # self.dataModel = GeneticModel()


def myExceptionhook(exc_type, exc_value, exc_traceback):
    log.critical("Unexpected exception occurred!",
                 exc_info=(exc_type, exc_value, exc_traceback))


def main(argv=sys.argv):
    sys.excepthook = myExceptionhook
    app = QApplication(argv)
    gui = LevyOptimalization()

    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()