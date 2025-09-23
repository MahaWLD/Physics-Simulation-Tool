from Pages.page import Page

from PyQt5 import QtCore, QtGui, QtWidgets

import pygame

from simulation import Simulation
from Pages.simulator_page import SimulatorPage


class PrebuiltModelsPage(Page):
    def __init__(self, stack, username):
        super().__init__()
        self.__stack = stack
        self.__username = username
        self.__initUI()

    def __initUI(self):
        super()._initUI()

        self.model_list = QtWidgets.QListWidget(self)
        self.model_list.setGeometry(QtCore.QRect(400, 280, 811, 301))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.model_list.setFont(font)

        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(QtCore.QRect(0, 90, 1601, 141))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(75, 50, 75, 75))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/BackButtonIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_button.setIcon(icon)
        self.back_button.setIconSize(QtCore.QSize(60, 60))

        self.title.setText("Pre-built Models")

        item = QtWidgets.QListWidgetItem()
        self.model_list.addItem(item)
        item = self.model_list.item(0)
        item.setText("Projectile Motion")

        self.__button_actions()

    def __button_actions(self):
        self.back_button.clicked.connect(lambda: self.__stack.setCurrentIndex(1))
        self.model_list.itemClicked.connect(self.__open_prebuilt_simulation)

    def __open_prebuilt_simulation(self, model):
        model = model.text()
        self.__stack.close()
        WIDTH, HEIGHT = 1600, 900
        window = pygame.display.set_mode((WIDTH, HEIGHT))

        # instance of the Simulation class
        simulation = Simulation(WIDTH, HEIGHT, window, self.__username)
        if model == "Projectile Motion":
            position_x = 150
            simulation.add_cannon(position_x)

        simulator_page = SimulatorPage(simulation)
        simulator_page.run()
