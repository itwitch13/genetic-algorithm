import logging
import time
import pandas as pd
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

from .ui.main_window import Ui_MainWindow
from src.population import Population
from src.example_functions import *

log = logging.getLogger(__name__)


class AppWindowWidget(QWidget, Ui_MainWindow):

    send_configurations = QtCore.pyqtSignal()
    send_plots = QtCore.pyqtSignal(list, list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Main Window constructor"""
        self.setupUi(self)

        self.onlyInt = QIntValidator()
        self.populationLineEdit.setValidator(self.onlyInt)
        self.generationLineEdit.setValidator(self.onlyInt)
        self.iterationLineEdit.setValidator(self.onlyInt)

        self.configuration_columns = ['Selection', 'Crossover', 'Mutation', 'Generations', 'Population', 'Time']
        self.df_configuration = pd.DataFrame([], columns=self.configuration_columns)

        self.init_input_types()
        self.get_parameters()
        self.iteratePushButton.clicked.connect(self.run_genetic_algorithm)

        # self.graphWidget.setBackground('w')
        self.graphValPushButton.clicked.connect(self.create_plots)

    def init_input_types(self):
        """
        Initializes types of selection, crossover, mutation.
        """
        selections = ['best_of_all_selection', 'roulette_wheel_selection', 'tournament_selection']
        self.selectionComboBox.addItems(selections)

        crossovers = ['crossover_one_point', 'crossover_two_point', 'crossover_homogenous']
        self.crossoverComboBox.addItems(crossovers)

        mutations = ['edge_mutation', 'one_point_mutation', 'two_points_mutation', 'inversion_mutation']
        self.mutationComboBox.addItems(mutations)

        self.populationLineEdit.setText(str(50))
        self.generationLineEdit.setText(str(50))
        self.mutationLineEdit.setText(str(0.01))
        self.xboundLineEdit.setText('-10,10')
        self.yboundLneEdit.setText('-10,10')
        self.iterationLineEdit.setText('0')

    def get_configurations(self):
        self.selection_type = str(self.selectionComboBox.currentText())
        self.crossover_type = str(self.crossoverComboBox.currentText())
        self.mutation_type = str(self.mutationComboBox.currentText())

    def get_parameters(self):
        self.population_size = int(self.populationLineEdit.text())
        self.generations = int(self.generationLineEdit.text())
        self.mutation_probability = float(self.mutationLineEdit.text())
        x_bound = self.xboundLineEdit.text()
        self.x_boundaries = [int(num) for num in x_bound.split(',')]
        y_bound = self.yboundLneEdit.text()
        self.y_boundaries = [int(num) for num in y_bound.split(',')]
        self.crossover_probability = 0.9
        self.elite_strategy_amount = 2
        self.percentage_selection = 0.03
        self.size_of_tournament = 3

    def binary_to_float(self, binary_value, border_a, border_b, m):
        combined_value = ''.join(map(str, binary_value))
        x = border_a + int(combined_value, 2) * (border_b - border_a) / (pow(2, m) - 1)
        return x

    def run_genetic_algorithm(self):
        start_time = time.clock()
        self.get_parameters()
        self.get_configurations()
        self.plot_x, self.plot_y, self.fx = [], [], []
        population = Population(booth_function, self.mutation_probability, self.crossover_probability,
                                self.elite_strategy_amount, self.population_size, self.x_boundaries,
                                self.y_boundaries)
        population.calculate_fitness()

        while self.generations != population.generations:

            population.get_configuration(self.mutation_type, self.crossover_type)
            population.selection(self.selection_type, self.percentage_selection, self.size_of_tournament)
            population.generate_new_population()
            population.calculate_fitness()
            print("generation: ", population.generations)
            for i in population.population:
                print(
                    f'x: {self.binary_to_float(i.x, self.x_boundaries[0], self.x_boundaries[1], len(i.x))} \
                    y: {self.binary_to_float(i.y, self.y_boundaries[0], self.y_boundaries[1], len(i.y))} '
                    f'f(x,y): {i.fitness}')

        execution_time = time.clock() - start_time
        self.plot_x, self.plot_y, self.fx = population.get_plots_parameters()
        self.timeLcdNumber.display(execution_time)
        self.save_configuration_to_file(execution_time)
        print('end')

    # def create_plots(self):
    #     g = gl.GLGridItem()
    #     g.scale(1, 1, 1)
    #     g.setDepthValue(100)  # draw grid after surfaces since they may be translucent
    #     self.graphWidget.addItem(g)
    #
    #     Z = np.ones((2, 2))
    #     p1 = gl.GLSurfacePlotItem(z=self.fx[49], shader='shaded', color=(0.5, 0.5, 1, 1))
    #     self.graphWidget.addItem(p1)
    #     self.graphWidget.plot(self.plot_x[49], self.plot_y[49])

    def create_plots(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        i = int(self.iterationLineEdit.text())-1

        x = np.linspace(min(self.plot_x[i]), max(self.plot_x[i]), 100)
        y = np.linspace(min(self.plot_y[i]), max(self.plot_y[i]), 100)
        x, y = np.meshgrid(x, y)
        z = (pow(x + 2 * y - 7, 2) + pow(2 * x + y - 5, 2))

        ax.plot_surface(x, y, z, color='g')
        plt.show()
        plt.savefig('plot3D.png')

    # def create_plot_matlib(self):
    #     # for 3D animation
    #     def data(i):
    #         ax.clear()
    #
    #         x = np.linspace(min(self.plot_x[i]), max(self.plot_x[i]), 100)
    #         y = np.linspace(min(self.plot_y[i]), max(self.plot_y[i]), 100)
    #         x, y = np.meshgrid(x, y)
    #         z = (pow(x + 2 * y - 7, 2) + pow(2 * x + y - 5, 2))
    #         line = ax.plot_surface(x, y, z, color='b')
    #         return line,
    #
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')
    #
    #     for i in range(len(self.plot_x)):
    #         anim = animation.FuncAnimation(fig, data, frames=len(self.plot_x), interval=30, blit=False)
    #         plt.close(anim._fig)
    #
    #         # plt.show()
    #         anim.save('temp.gif', writer=animation.PillowWriter())

    def save_configuration_to_file(self, time):
        config = [self.selection_type, self.crossover_type, self.mutation_type,
                  self.generations, self.population_size, time]
        config_series = pd.Series(config, index=self.df_configuration.columns)
        self.df_configuration = self.df_configuration.append(config_series, ignore_index=True)

        with pd.ExcelWriter('configurations_param.xlsx') as writer:
            self.df_configuration.to_excel(writer, sheet_name='Parameters', index=False)
