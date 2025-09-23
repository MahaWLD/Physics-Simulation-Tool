from Pages.page import Page

from PyQt5 import QtCore, QtGui, QtWidgets

from database import cursor

import pygame

from simulation import Simulation
from Pages.simulator_page import SimulatorPage


class SavedProjectsPage(Page):
    def __init__(self, stack, username):
        super().__init__()
        self.__stack = stack
        self.__username = username
        self.__initUI()

    def __initUI(self):
        super()._initUI()

        self.project_list = QtWidgets.QListWidget(self)
        self.project_list.setGeometry(QtCore.QRect(400, 280, 811, 301))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.project_list.setFont(font)

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

        self.title.setText("Saved Projects")

        self.__get_saved_projects()
        self.__button_actions()

    def __button_actions(self):
        self.back_button.clicked.connect(lambda: self.__stack.setCurrentIndex(1))
        self.project_list.itemClicked.connect(self.__open_project)

    def __get_saved_projects(self):
        try:
            query = "SELECT project_name FROM SavedProjects WHERE userID = %s"
            cursor.execute(query, (self.__username,))
            project_names = [row[0] for row in cursor.fetchall()]
            i = 0
            for project in project_names:
                item = QtWidgets.QListWidgetItem()
                self.project_list.addItem(item)  # create list item
                item.setText(project)  # name list item
                i += 1
        except Exception as e:
            print(e)

    def __open_project(self, project):
        project_name = project.text()
        self.__stack.close()
        WIDTH, HEIGHT = 1600, 900
        window = pygame.display.set_mode((WIDTH, HEIGHT))

        # instance of the Simulation class
        simulation = Simulation(WIDTH, HEIGHT, window, self.__username)
        simulation.load_project(project_name)

        simulator_page = SimulatorPage(simulation)
        simulator_page.run()
