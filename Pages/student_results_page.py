from Pages.page import Page
from PyQt5 import QtCore, QtGui, QtWidgets

from database import cursor


class StudentProgressPage(Page):
    def __init__(self, stack):
        super().__init__()
        self.__stack = stack
        self.__initUI()

    def __initUI(self):
        super()._initUI()
        self.title = QtWidgets.QLabel(self)
        self.title.setEnabled(True)
        self.title.setGeometry(QtCore.QRect(0, 50, 1601, 171))
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

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(75, 50, 75, 75))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/BackButtonIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_button.setIcon(icon)
        self.back_button.setIconSize(QtCore.QSize(60, 60))

        self.student_results_table = QtWidgets.QTableWidget(self)
        self.student_results_table.setGeometry(QtCore.QRect(810, 250, 511, 491))
        self.student_results_table.setColumnCount(4)
        self.student_results_table.setHorizontalHeaderLabels(["Question Number", "User ID", "Answer", "Result"])

        self.question_table = QtWidgets.QTableWidget(self)
        self.question_table.setGeometry(QtCore.QRect(210, 250, 521, 491))
        self.question_table.setColumnCount(4)
        self.question_table.setHorizontalHeaderLabels(["Question Number", "Model", "Difficulty Level", "Question"])

        self.title.setText("Student Progress")

        self.__populate_question_table()
        self.__populate_student_results_table()
        self.__button_actions()

    def __populate_question_table(self):
        self.question_table.clear()  # clear table
        query = "SELECT * FROM Questions"
        cursor.execute(query)
        questions = cursor.fetchall()

        self.question_table.setRowCount(len(questions))
        for i, question in enumerate(questions):
            for j, data in enumerate(question):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.question_table.setItem(i, j, item)

    def __populate_student_results_table(self):
        self.student_results_table.clear()  # clear table
        query = "SELECT * FROM ProgressTracker"
        cursor.execute(query)
        results = cursor.fetchall()

        self.student_results_table.setRowCount(len(results))
        for i, result in enumerate(results):
            for j, data in enumerate(result):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.student_results_table.setItem(i, j, item)

    def __button_actions(self):
        self.back_button.clicked.connect(lambda: self.__stack.setCurrentIndex(1))
