from Pages.page import Page

from PyQt5 import QtCore, QtGui, QtWidgets

from Pages.add_user_window import AddUser
from Pages.main_menu import MainMenu
from Pages.saved_projects_page import SavedProjectsPage
from Pages.prebuilt_models_page import PrebuiltModelsPage


class LoginPage(Page):
    def __init__(self, stack):
        super().__init__()
        self.__stack = stack
        self.__initUI()

    def __initUI(self):
        super()._initUI()

        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(QtCore.QRect(0, 180, 1601, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.guest_mode_button = QtWidgets.QPushButton(self)
        self.guest_mode_button.setGeometry(QtCore.QRect(30, 800, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.guest_mode_button.setFont(font)

        self.sign_in_button = QtWidgets.QPushButton(self)
        self.sign_in_button.setGeometry(QtCore.QRect(730, 270, 201, 281))

        self.sign_in_label = QtWidgets.QLabel(self)
        self.sign_in_label.setGeometry(QtCore.QRect(790, 470, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.sign_in_label.setFont(font)
        self.sign_in_label.setAlignment(QtCore.Qt.AlignCenter)

        self.new_user_icon = QtWidgets.QLabel(self)
        self.new_user_icon.setGeometry(QtCore.QRect(770, 320, 121, 121))
        self.new_user_icon.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.new_user_icon.setText("")
        self.new_user_icon.setPixmap(QtGui.QPixmap("Images/Login/AddUserIcon.png"))
        self.new_user_icon.setScaledContents(True)

        self.title.setText("Who\'s using Physics Simulation Tool?")
        self.guest_mode_button.setText("Guest Mode")
        self.sign_in_label.setText("Sign in")

        self.__button_actions()

    def __button_actions(self):
        self.sign_in_button.clicked.connect(self.__show_add_user_window)
        self.guest_mode_button.clicked.connect(self.__guest_login)

    def __show_add_user_window(self):
        # instantiate and show add user window
        add_user_window = AddUser(self.__stack)  # composition
        add_user_window.show()

    def __guest_login(self):
        # instantiate page classes
        main_menu = MainMenu(self.__stack, username='Guest')
        self.__stack.addWidget(main_menu)

        saved_projects_page = SavedProjectsPage(self.__stack, username='Guest')
        self.__stack.addWidget(saved_projects_page)

        prebuilt_models_page = PrebuiltModelsPage(self.__stack, username='Guest')
        self.__stack.addWidget(prebuilt_models_page)

        self.__stack.setCurrentIndex(1)     # continue to main menu
