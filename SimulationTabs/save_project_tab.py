from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class SaveProject(QWidget):
    def __init__(self, simulation):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 336, 194
        self.__simulation = simulation
        self.__initUI()

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #d1dbe3")
        self.setWindowTitle("Save project")

        self.save_button_box = QtWidgets.QDialogButtonBox(self)
        self.save_button_box.setGeometry(QtCore.QRect(90, 120, 151, 61))
        self.save_button_box.setStyleSheet("background-color: #ffffff")
        self.save_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)

        self.save_label = QtWidgets.QLabel(self)
        self.save_label.setGeometry(QtCore.QRect(30, 20, 241, 31))

        font = QtGui.QFont()
        font.setPointSize(16)

        self.save_label.setFont(font)

        self.project_name_text_edit = QtWidgets.QPlainTextEdit(self)
        self.project_name_text_edit.setGeometry(QtCore.QRect(50, 70, 231, 31))

        font = QtGui.QFont()
        font.setPointSize(11)

        self.project_name_text_edit.setFont(font)
        self.project_name_text_edit.setStyleSheet("background-color: #ffffff")

        self.invalid_label = QtWidgets.QLabel(self)
        self.invalid_label.setGeometry(QtCore.QRect(55, 105, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.invalid_label.setFont(font)

        self.save_label.setText("Save project as:")

        self.__button_actions()

    def __button_actions(self):
        self.save_button_box.accepted.connect(self.__save)
        self.save_button_box.rejected.connect(self.close)

    def __save(self):
        project_name = self.project_name_text_edit.toPlainText()
        if project_name != "":
            self.__simulation.save_as_project(project_name)
            self.close()
        else:
            self.invalid_label.setText("Invalid name")
