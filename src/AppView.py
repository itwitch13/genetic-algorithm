import logging
import time
import pandas as pd

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.main_window import Ui_MainWindow
from src.population import Population
from src.example_functions import *

log = logging.getLogger(__name__)


class AppWindowWidget(QWidget, Ui_MainWindow):

    send_configurations = QtCore.pyqtSignal()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Main Window constructor"""
        self.setupUi(self)

        self.onlyInt = QIntValidator()
        self.populationLineEdit.setValidator(self.onlyInt)
        self.generationLineEdit.setValidator(self.onlyInt)

        self.configuration_columns = ['Selection', 'Crossover', 'Mutation', 'Generations', 'Population', 'Time']
        self.df_configuration = pd.DataFrame([], columns=self.configuration_columns)

        self.init_input_types()
        self.get_parameters()
        self.iteratePushButton.clicked.connect(self.run_genetic_algorithm)

    def init_input_types(self):
        """
        Initializes types of selection, crossover, mutation.
        """
        selections = ['Rank', 'Roulette Wheel', 'Tournament', 'Elitism']
        self.selectionComboBox.addItems(selections)

        crossovers = ['Single-point', 'Two-point', 'Three-point', 'Uniform']
        self.crossoverComboBox.addItems(crossovers)

        mutations = ['Boundary', 'Single Bit Flip', 'Two Bit Flip', 'Inversion']
        self.mutationComboBox.addItems(mutations)

        self.populationLineEdit.setText(str(50))
        self.generationLineEdit.setText(str(50))
        self.mutationLineEdit.setText(str(0.01))
        self.xboundLineEdit.setText('-100,100')
        self.yboundLneEdit.setText('-100,100')

    def get_configurations(self):
        self.selection = str(self.selectionComboBox.currentText())
        self.crossover = str(self.crossoverComboBox.currentText())
        self.mutation = str(self.mutationComboBox.currentText())
        # self.send_configurations.emit(selection, crossover, mutation)

    def get_parameters(self):
        self.population_size = int(self.populationLineEdit.text())
        self.generations = int(self.generationLineEdit.text())
        self.mutation_rate = float(self.mutationLineEdit.text())
        x_bound = self.xboundLineEdit.text()
        self.x_boundaries = [int(num) for num in x_bound.split(',')]
        y_bound = self.yboundLneEdit.text()
        self.y_boundaries = [int(num) for num in y_bound.split(',')]

    def run_genetic_algorithm(self):
        start_time = time.clock()

        self.get_parameters()
        self.get_configurations()
        population = Population(booth_function, self.mutation_rate, self.population_size,
                                self.x_boundaries, self.y_boundaries)
        population.calculate_fitness()
        while self.generations != population.generations:

            population.best_of_all_selection(percentage=0.3)
            population.generate_new_population()
            population.calculate_fitness()
            print(population.generations)
            for i in population.population:
                print(f'x: {i.x} y: {i.y} f(x,y): {i.fitness}')

        execution_time = time.clock() - start_time
        self.timeLcdNumber.display(execution_time)
        self.save_configuration_to_file(execution_time)

    def save_configuration_to_file(self, time):
        config = [self.selection, self.crossover, self.mutation, self.generations, self.population_size, time]
        config_series = pd.Series(config, index=self.df_configuration.columns)
        self.df_configuration = self.df_configuration.append(config_series, ignore_index=True)

        with pd.ExcelWriter('configurations_param.xlsx') as writer:
            self.df_configuration.to_excel(writer, sheet_name='Parameters', index=False)
