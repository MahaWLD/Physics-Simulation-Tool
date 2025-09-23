import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
import pygame

from Pages.login_page import LoginPage
from simulation import Simulation
from Pages.simulator_page import SimulatorPage


def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()  # instance of the page class

    login_page = LoginPage(stack)   # instance of the login page class
    stack.addWidget(login_page)  # adding login page to page stack

    stack.setWindowTitle("Physics Simulation Tool")
    stack.show()

    # quit Pygame when the simulation ends
    pygame.quit()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
