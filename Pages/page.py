from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore, QtGui, QtWidgets

import pygame

from Pages.settings import Settings


class Page(QMainWindow):
    def __init__(self):
        super().__init__()
        self._WIDTH, self._HEIGHT = 1600, 900
        self.settings_window = Settings(self)
        self.settings_window.show_grid = True
        self.__step = 0
        self.__PAGE_BG_COLOUR = 180, 206, 222
        self._initUI()

    def _initUI(self):
        self.setGeometry(100, 100, self._WIDTH, self._HEIGHT)
        self.py_surface = pygame.Surface((self._WIDTH, self._HEIGHT))

        # central widget and layout to place the elements upon
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # PyQt5 elements
        self.label = QLabel(self)
        self.label.setFixedSize(self._WIDTH, self._HEIGHT)
        self.layout.addWidget(self.label)

        # QTimer to update the Pygame surface and PyQt5 label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._grid)
        self.timer.start(1000 // 60)  # update every 1/60th of a second (60 FPS)

        self.settings_button = QtWidgets.QPushButton(self)
        self.settings_button.setGeometry(QtCore.QRect(1420, 710, 75, 75))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/Simulator/Icons/SettingsIcon.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)

        self.settings_button.setIcon(icon)
        self.settings_button.setIconSize(QtCore.QSize(75, 75))

        self.__button_actions()

    def __button_actions(self):
        self.settings_button.clicked.connect(self._toggle_settings)

    def _grid(self):
        if self.settings_window.dark_mode:
            self.__PAGE_BG_COLOUR = 9, 16, 29   # changing page background colour when dark mode toggled
        else:
            self.__PAGE_BG_COLOUR = 180, 206, 222

        self.py_surface.fill(self.__PAGE_BG_COLOUR)

        if self.settings_window.show_grid:

            for x in range(0 - self.__step, self._WIDTH, 50):
                pygame.draw.line(self.py_surface, (43, 90, 179), (x, 0), (x, self._HEIGHT))
            for y in range(0, self._HEIGHT, 50):
                pygame.draw.line(self.py_surface, (43, 90, 179), (0, y), (self._WIDTH, y))

            self.__step += 1    # change position of grid lines
            if self.__step >= 50:
                self.__step = 0     # reset

        img = QImage(self.py_surface.get_buffer(), self._WIDTH, self._HEIGHT, QImage.Format_RGB32)
        pixmap = QPixmap.fromImage(img)
        self.label.setPixmap(pixmap)

    def _toggle_settings(self):
        self.settings_window.show()
