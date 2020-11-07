import logging

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.main_window import Ui_MainWindow

log = logging.getLogger(__name__)


class AppWindowWidget(QWidget, Ui_MainWindow):

    send_configurations = QtCore.pyqtSignal()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Main Window constructor"""
        self.setupUi(self)

        self.init_input_types()
        self.iteratePushButton.clicked.connect(self.get_configurations)


    def init_input_types(self):
        """
        Initializes types of selection, crossover, mutation.
        """
        selections = []
        for item in selections:
            self.selectionComboBox.addItems(item)

        crossovers = []
        for item in crossovers:
            self.crossoverComboBox.addItems(item)

        mutations = []
        for item in mutations:
            self.mutationsComboBox.addItems(item)

        # self.iterateLineEdit.setText("Generations...")

    def get_configurations(self):
        selection = str(self.selectionComboBox.currentText())
        crossover = str(self.crossoverComboBox.currentText())
        mutation = str(self.mutationComboBox.currentText())
        generation = str(self.iterateLineEdit)
        self.send_configurations.emit(generation, selection, crossover, mutation)

