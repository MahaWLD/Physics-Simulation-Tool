from Pages.page import Page
from PyQt5 import QtCore, QtGui, QtWidgets

import pygame

from simulation import Simulation
from Pages.simulator_page import SimulatorPage

from database import cursor


class MainMenu(Page):
    def __init__(self, stack, username):
        super().__init__()
        self.__stack = stack
        self.__username = username
        self.__account_type = None
        self.settings_window.set_username(username)

        if self.__username != "Guest":
            query = "SELECT account_type FROM Credentials WHERE username = %s"
            cursor.execute(query, (self.__username,))
            self.__account_type = cursor.fetchone()[0]

        self.__initUI()
        self.__set_username_text(username)

    def __initUI(self):
        super()._initUI()

        self.title = QtWidgets.QLabel(self)
        self.title.setEnabled(True)
        self.title.setGeometry(QtCore.QRect(0, 90, 1601, 171))

        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)

        self.title.setFont(font)
        self.title.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title.setAutoFillBackground(False)
        self.title.setTextFormat(QtCore.Qt.PlainText)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(250, 260, 1081, 271))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.new_project_button = QtWidgets.QPushButton(self.frame)
        self.new_project_button.setGeometry(QtCore.QRect(30, 40, 331, 181))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

        self.new_project_button.setPalette(palette)
        self.new_project_button.setText("")
        self.new_project_button.setCheckable(False)

        self.new_file_icon = QtWidgets.QLabel(self.frame)
        self.new_file_icon.setGeometry(QtCore.QRect(140, 50, 111, 111))
        self.new_file_icon.setText("")
        self.new_file_icon.setPixmap(QtGui.QPixmap("Images/Main Menu/NewFileIcon.png"))
        self.new_file_icon.setScaledContents(True)

        self.new_project_label = QtWidgets.QLabel(self.frame)
        self.new_project_label.setGeometry(QtCore.QRect(100, 150, 191, 71))

        font = QtGui.QFont()
        font.setPointSize(24)

        self.new_project_label.setFont(font)
        self.new_project_label.setAlignment(QtCore.Qt.AlignCenter)

        self.load_project_button = QtWidgets.QPushButton(self.frame)
        self.load_project_button.setGeometry(QtCore.QRect(380, 40, 331, 181))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

        self.load_project_button.setPalette(palette)
        self.load_project_button.setText("")
        self.load_project_button.setCheckable(False)

        self.load_project_icon = QtWidgets.QLabel(self.frame)
        self.load_project_icon.setGeometry(QtCore.QRect(490, 50, 111, 111))
        self.load_project_icon.setText("")
        self.load_project_icon.setPixmap(QtGui.QPixmap("Images/Main Menu/LoadFileIcon.png"))
        self.load_project_icon.setScaledContents(True)

        self.load_project_label = QtWidgets.QLabel(self.frame)
        self.load_project_label.setGeometry(QtCore.QRect(450, 150, 191, 71))

        font = QtGui.QFont()
        font.setPointSize(24)

        self.load_project_label.setFont(font)
        self.load_project_label.setAlignment(QtCore.Qt.AlignCenter)

        self.prebuilt_models_button = QtWidgets.QPushButton(self.frame)
        self.prebuilt_models_button.setGeometry(QtCore.QRect(730, 40, 331, 181))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(202, 202, 202))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

        self.prebuilt_models_button.setPalette(palette)
        self.prebuilt_models_button.setText("")
        self.prebuilt_models_button.setCheckable(False)

        self.prebuilt_models_icon = QtWidgets.QLabel(self.frame)
        self.prebuilt_models_icon.setGeometry(QtCore.QRect(840, 70, 101, 71))
        self.prebuilt_models_icon.setText("")
        self.prebuilt_models_icon.setPixmap(QtGui.QPixmap("Images/Main Menu/Pre-builtIcon.png"))
        self.prebuilt_models_icon.setScaledContents(True)

        self.prebuilt_models_label = QtWidgets.QLabel(self.frame)
        self.prebuilt_models_label.setGeometry(QtCore.QRect(780, 150, 231, 71))

        font = QtGui.QFont()
        font.setPointSize(24)

        self.prebuilt_models_label.setFont(font)
        self.prebuilt_models_label.setAlignment(QtCore.Qt.AlignCenter)

        self.account_toolbox = QtWidgets.QToolBox(self)
        self.account_toolbox.setGeometry(QtCore.QRect(80, 660, 281, 131))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(186, 228, 236))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(186, 228, 236))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(186, 228, 236))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

        self.account_toolbox.setPalette(palette)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)

        self.account_toolbox.setFont(font)

        self.AccountInfo = QtWidgets.QWidget()
        self.AccountInfo.setGeometry(QtCore.QRect(0, 0, 281, 75))

        self.user_icon = QtWidgets.QLabel(self.AccountInfo)
        self.user_icon.setGeometry(QtCore.QRect(30, 10, 51, 51))
        self.user_icon.setText("")
        self.user_icon.setPixmap(QtGui.QPixmap("Images/Login/ExistingUserIcon.png"))
        self.user_icon.setScaledContents(True)

        self.username_label = QtWidgets.QLabel(self.AccountInfo)
        self.username_label.setGeometry(QtCore.QRect(90, 10, 181, 51))

        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)

        self.username_label.setFont(font)

        self.account_toolbox.addItem(self.AccountInfo, "")

        self.Logout = QtWidgets.QWidget()
        self.Logout.setGeometry(QtCore.QRect(0, 0, 281, 75))

        self.logout_button = QtWidgets.QPushButton(self.Logout)
        self.logout_button.setGeometry(QtCore.QRect(50, 16, 191, 41))

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)

        self.logout_button.setFont(font)

        self.account_toolbox.addItem(self.Logout, "")

        self.guest_message = QtWidgets.QLabel(self)
        self.guest_message.setGeometry(QtCore.QRect(630, 500, 331, 41))

        font = QtGui.QFont()
        font.setPointSize(16)

        self.guest_message.setFont(font)
        self.guest_message.setAlignment(QtCore.Qt.AlignCenter)

        self.title.setText("Physics Simulation Tool")
        self.new_project_label.setText("New Project")
        self.load_project_label.setText("Load Project")
        self.prebuilt_models_label.setText("Pre-built Models")
        self.logout_button.setText("Log out")

        self.account_toolbox.setItemText(0, "Account")
        self.account_toolbox.setItemText(1, "Log out")

        if self.__account_type == "T":
            self.__teacher_account_buttons()

        self.__button_actions()

    def __teacher_account_buttons(self):
        self.question_editor_button = QtWidgets.QPushButton(self)
        self.question_editor_button.setGeometry(QtCore.QRect(560, 650, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.question_editor_button.setFont(font)

        self.student_progress_button = QtWidgets.QPushButton(self)
        self.student_progress_button.setGeometry(QtCore.QRect(820, 650, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.student_progress_button.setFont(font)

        self.question_editor_button.setText("Question Editor")
        self.student_progress_button.setText("Student Progress")

    def __button_actions(self):
        self.new_project_button.clicked.connect(self.__open_new_project)
        self.load_project_button.clicked.connect(self.__open_saved_projects)
        self.prebuilt_models_button.clicked.connect(self.__open_prebuilt_models)
        self.logout_button.clicked.connect(self.__logout)

        if self.__account_type == "T":
            self.question_editor_button.clicked.connect(self.__open_question_editor)
            self.student_progress_button.clicked.connect(self.__open_student_progress)

    def __open_new_project(self):
        self.__stack.close()
        WIDTH, HEIGHT = 1600, 900
        window = pygame.display.set_mode((WIDTH, HEIGHT))

        # instance of the Simulation class
        simulation = Simulation(WIDTH, HEIGHT, window, self.__username)

        simulator_page = SimulatorPage(simulation)
        simulator_page.run()

    def __open_saved_projects(self):
        if self.__username == "Guest":
            self.guest_message.setText("Sign in to access saved projects")
        else:
            self.__stack.setCurrentIndex(2)

    def __open_prebuilt_models(self):
        self.__stack.setCurrentIndex(3)

    def __set_username_text(self, username):
        self.username_label.setText(username)

    def __logout(self):
        self.__stack.setCurrentIndex(0)
        self.__username = None

    def __open_question_editor(self):
        self.__stack.setCurrentIndex(4)

    def __open_student_progress(self):
        self.__stack.setCurrentIndex(5)
