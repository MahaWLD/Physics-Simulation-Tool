from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

import mysql.connector
from database import cursor, db

from Pages.main_menu import MainMenu
from Pages.saved_projects_page import SavedProjectsPage
from Pages.prebuilt_models_page import PrebuiltModelsPage
from Pages.question_editor_page import QuestionEditorPage
from Pages.student_results_page import StudentProgressPage

import hashlib


class AddUser(QMainWindow):
    def __init__(self, stack):
        super().__init__(stack)
        self.__stack = stack
        self.__WIDTH, self.__HEIGHT = 800, 450
        self.__account_type = "S"     # student account by default
        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("Add User")
        self.setGeometry(100, 100, self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #d1dbe3;")

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 781, 431))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("background-color: #d1dbe3")

        self.LoginTab = QtWidgets.QWidget()

        self.login_button = QtWidgets.QPushButton(self.LoginTab)
        self.login_button.setGeometry(QtCore.QRect(330, 250, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("background-color: #ffffff")

        self.password_label = QtWidgets.QLabel(self.LoginTab)
        self.password_label.setGeometry(QtCore.QRect(230, 120, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.password_label.setFont(font)

        self.username_entry = QtWidgets.QLineEdit(self.LoginTab)
        self.username_entry.setGeometry(QtCore.QRect(370, 80, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.username_entry.setFont(font)
        self.username_entry.setStyleSheet("background-color: #ffffff")

        self.password_entry = QtWidgets.QLineEdit(self.LoginTab)
        self.password_entry.setGeometry(QtCore.QRect(370, 120, 191, 31))
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_entry.setFont(font)
        self.password_entry.setStyleSheet("background-color: #ffffff")

        self.invalid_label = QtWidgets.QLabel(self.LoginTab)
        self.invalid_label.setGeometry(QtCore.QRect(230, 160, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.invalid_label.setFont(font)
        self.invalid_label.setAlignment(QtCore.Qt.AlignCenter)

        self.username_label = QtWidgets.QLabel(self.LoginTab)
        self.username_label.setGeometry(QtCore.QRect(230, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.username_label.setFont(font)

        self.tabWidget.addTab(self.LoginTab, "Login")

        self.SignupTab = QtWidgets.QWidget()

        self.password_label_2 = QtWidgets.QLabel(self.SignupTab)
        self.password_label_2.setGeometry(QtCore.QRect(210, 120, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.password_label_2.setFont(font)

        self.password_entry_2 = QtWidgets.QLineEdit(self.SignupTab)
        self.password_entry_2.setGeometry(QtCore.QRect(400, 120, 191, 31))
        self.password_entry_2.setEchoMode(QtWidgets.QLineEdit.Password)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_entry_2.setFont(font)
        self.password_entry_2.setStyleSheet("background-color: #ffffff")

        self.username_entry_2 = QtWidgets.QLineEdit(self.SignupTab)
        self.username_entry_2.setGeometry(QtCore.QRect(400, 80, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.username_entry_2.setFont(font)
        self.username_entry_2.setStyleSheet("background-color: #ffffff")

        self.register_button = QtWidgets.QPushButton(self.SignupTab)
        self.register_button.setGeometry(QtCore.QRect(330, 270, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.register_button.setFont(font)
        self.register_button.setStyleSheet("background-color: #ffffff")

        self.confirm_password_label = QtWidgets.QLabel(self.SignupTab)
        self.confirm_password_label.setGeometry(QtCore.QRect(210, 160, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.confirm_password_label.setFont(font)

        self.confirm_password_entry = QtWidgets.QLineEdit(self.SignupTab)
        self.confirm_password_entry.setGeometry(QtCore.QRect(400, 160, 191, 31))
        self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm_password_entry.setFont(font)
        self.confirm_password_entry.setStyleSheet("background-color: #ffffff")

        self.invalid_label_2 = QtWidgets.QLabel(self.SignupTab)
        self.invalid_label_2.setGeometry(QtCore.QRect(210, 200, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.invalid_label_2.setFont(font)
        self.invalid_label_2.setAlignment(QtCore.Qt.AlignCenter)

        self.username_label_2 = QtWidgets.QLabel(self.SignupTab)
        self.username_label_2.setGeometry(QtCore.QRect(210, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.username_label_2.setFont(font)

        self.student_button = QtWidgets.QPushButton(self.SignupTab)
        self.student_button.setGeometry(QtCore.QRect(560, 340, 81, 23))
        self.student_button.setStyleSheet("background-color: #9ba2a8")

        self.teacher_button = QtWidgets.QPushButton(self.SignupTab)
        self.teacher_button.setGeometry(QtCore.QRect(640, 340, 81, 23))
        self.teacher_button.setStyleSheet("background-color: #ffffff")

        self.tabWidget.addTab(self.SignupTab, "Sign up")

        self.login_button.setText("Login")
        self.password_label.setText("Password:")
        self.username_label.setText("Username:")
        self.password_label_2.setText("Password:")
        self.username_label_2.setText("Username:")
        self.register_button.setText("Register")
        self.confirm_password_label.setText("Confirm password:")
        self.student_button.setText("Student")
        self.teacher_button.setText("Teacher")

        self.__button_actions()

    def __button_actions(self):
        self.login_button.clicked.connect(self.__login)
        self.register_button.clicked.connect(self.__signup)

        self.student_button.clicked.connect(self.__edit_account_type)
        self.teacher_button.clicked.connect(self.__edit_account_type)

    def __edit_account_type(self):
        button = self.sender()

        if button == self.student_button:
            self.student_button.setStyleSheet("background-color: #9ba2a8")
            self.teacher_button.setStyleSheet("background-color: #ffffff")
            self.__account_type = "S"   # student
        else:
            self.student_button.setStyleSheet("background-color: #ffffff")
            self.teacher_button.setStyleSheet("background-color: #9ba2a8")
            self.__account_type = "T"   # teacher

    # LOGIN LOGIC

    def __login(self):
        # fetch username and password
        username = self.username_entry.text()
        password = self.password_entry.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # hash password

        if username == "":
            self.invalid_label.setText("Enter a username")
            return

        # find username in Credentials table
        query = "SELECT * FROM Credentials WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[1]
            if hashed_password == stored_password:  # if password entered matches password in database
                print("[Login successful]")
                account_type = user[2]  # assign account type
                self.__create_pages(username)
                if account_type == "T":
                    self.__create_teacher_pages()
                self.close()
                self.__stack.setCurrentIndex(1)  # continue to main menu
            else:
                self.invalid_label.setText("Password incorrect")
        else:
            self.invalid_label.setText("Username not found")

    def __signup(self):
        username = self.username_entry_2.text()
        password = self.password_entry_2.text()
        confirm_password = self.confirm_password_entry.text()

        if username == "":
            self.invalid_label_2.setText("Enter a username")
            return

        if username == "Guest":
            self.invalid_label_2.setText("Invalid username")
            return

        if password == "":
            self.invalid_label_2.setText("Enter a password")
            return

        if password != confirm_password:
            self.invalid_label_2.setText("Passwords do not match")
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            try:
                query = "INSERT INTO Credentials (username, password, account_type) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, hashed_password, self.__account_type))
                db.commit()
                print("[Signup successful]")

                self.__create_pages(username)

                if self.__account_type == "T":
                    self.__create_teacher_pages()

                self.close()

                self.__stack.setCurrentIndex(1)
            except mysql.connector.Error as e:
                print("Error during signup:", e)
                # error is likely that there is already a username in the database
                # resulting in a primary key that is not unique
                self.invalid_label_2.setText("Username already exists - pick another")

    def __create_pages(self, username):
        # instantiate default pages and pass in username
        main_menu = MainMenu(self.__stack, username)
        self.__stack.addWidget(main_menu)

        saved_projects_page = SavedProjectsPage(self.__stack, username)
        self.__stack.addWidget(saved_projects_page)

        prebuilt_models_page = PrebuiltModelsPage(self.__stack, username)
        self.__stack.addWidget(prebuilt_models_page)

    def __create_teacher_pages(self):
        # instantiate teacher pages
        question_editor_page = QuestionEditorPage(self.__stack)
        self.__stack.addWidget(question_editor_page)

        student_progress_page = StudentProgressPage(self.__stack)
        self.__stack.addWidget(student_progress_page)
