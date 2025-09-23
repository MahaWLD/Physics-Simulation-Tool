import pygame

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Graph:
    def __init__(self, simulation, max_points=20):
        self.__simulation = simulation
        self.__max_points = max_points
        self.__data_queue = []
        self.__surface = pygame.Surface((400, 200))
        self.__rect = self.__surface.get_rect(topleft=(1000, 675))
        self.show_graph = False
        self.max_value = None

    def toggle_graph(self):
        self.show_graph = not self.show_graph

    def update_plot(self, data):
        if self.__simulation.resume:
            self.__data_queue.append(data)
            if len(self.__data_queue) > self.__max_points:
                self.__data_queue.pop(0)  # remove first value
            if data > self.max_value:  # increase max_value if data exceeds current max_value
                self.max_value = data
            self.__draw(self.max_value)

    def __draw(self, max_value):
        self.__surface.fill("white")  # clear graph surface

        # draw graph line
        points = []
        for i, d in enumerate(self.__data_queue):
            x = i * self.__rect.width / self.__max_points
            y = self.__rect.height / 2 - (d / max_value) * self.__rect.height / 2
            points.append((x, y))
        if len(points) >= 2:
            pygame.draw.lines(self.__surface, (0, 0, 255), False, points, 2)

        # draw x-axis
        pygame.draw.line(self.__surface, (0, 0, 0), (0, self.__rect.height // 2), (self.__rect.width, self.__rect.height // 2), 2)

        # draw y-axis
        pygame.draw.line(self.__surface, (0, 0, 0), (0, 0), (0, self.__rect.height), 2)

        # draw y-axis scale
        scale_font = pygame.font.SysFont("Calibre", 16)
        scale_label = scale_font.render(f"Max Value: {max_value:.2f}", True, (0, 0, 0))
        self.__surface.blit(scale_label, (10, 0))

    def draw_on(self, screen):
        if self.show_graph:
            screen.blit(self.__surface, self.__rect.topleft)


class GraphDataInput(QWidget):
    def __init__(self, simulation):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 460, 212
        self.__simulation = simulation
        self.graph = Graph(simulation)
        self.object_selected = None
        self.variable = None
        self.__initUI()

        self.max_graph_value = {
            "Height": 15,
            "Velocity": 100,
            "Vertical velocity": 100,
            "Horizontal velocity": 100,
            "Kinetic energy": 1000,
            "Gravitational potential energy": 1000
        }

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #d1dbe3")
        self.setWindowTitle("Graph Input")

        self.object_selected_label = QtWidgets.QLabel(self)
        self.object_selected_label.setGeometry(QtCore.QRect(40, 30, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.object_selected_label.setFont(font)

        self.variable_label = QtWidgets.QLabel(self)
        self.variable_label.setGeometry(QtCore.QRect(40, 70, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.variable_label.setFont(font)

        self.plot_button = QtWidgets.QPushButton(self)
        self.plot_button.setGeometry(QtCore.QRect(230, 130, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.plot_button.setFont(font)
        self.plot_button.setStyleSheet("background-color: #ffffff")

        self.update_object_list_button = QtWidgets.QPushButton(self)
        self.update_object_list_button.setGeometry(QtCore.QRect(60, 140, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.update_object_list_button.setFont(font)
        self.update_object_list_button.setStyleSheet("background-color: #ffffff")

        self.variable_combobox = QtWidgets.QComboBox(self)
        self.variable_combobox.setGeometry(QtCore.QRect(220, 70, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.variable_combobox.setFont(font)
        self.variable_combobox.setStyleSheet("background-color: #ffffff")

        self.object_selected_combobox = QtWidgets.QComboBox(self)
        self.object_selected_combobox.setGeometry(QtCore.QRect(220, 30, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.object_selected_combobox.setFont(font)
        self.object_selected_combobox.setStyleSheet("background-color: #ffffff")

        self.object_selected_label.setText("Object selected:")
        self.variable_label.setText("Variable to plot:")
        self.update_object_list_button.setText("Update object list")
        self.plot_button.setText("Plot graph")

        self.__update_object_combobox()

        self.variable_combobox.addItem("Height")
        self.variable_combobox.addItem("Velocity")
        self.variable_combobox.addItem("Vertical velocity")
        self.variable_combobox.addItem("Horizontal velocity")
        self.variable_combobox.addItem("Kinetic energy")
        self.variable_combobox.addItem("Gravitational potential energy")

        self.__button_actions()

    def __button_actions(self):
        self.plot_button.clicked.connect(self.__plot_graph)
        self.update_object_list_button.clicked.connect(self.__update_object_combobox)

    def __plot_graph(self):
        self.object_selected = self.__find_object_selected()
        self.variable = self.variable_combobox.currentText()
        self.graph.max_value = self.max_graph_value[self.variable]

    def __find_object_selected(self):  # linear search
        obj_name = self.object_selected_combobox.currentText()
        items = self.__simulation.objects + self.__simulation.models
        for obj in items:
            if obj_name == obj.name:
                object_selected = obj
                return object_selected

    def __update_object_combobox(self):
        self.object_selected_combobox.clear()

        for obj in self.__simulation.objects:
            self.object_selected_combobox.addItem(obj.name)
