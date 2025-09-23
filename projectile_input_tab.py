from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class ProjectileInput(QWidget):
    def __init__(self, simulation, cannon, projectile):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 336, 297
        self.__simulation = simulation
        self.__cannon = cannon
        self.__projectile = projectile
        self.__initUI()

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #d1dbe3")
        self.setWindowTitle("Projectile input")

        self.confirm_button_box = QtWidgets.QDialogButtonBox(self)
        self.confirm_button_box.setGeometry(QtCore.QRect(90, 230, 151, 61))
        self.confirm_button_box.setStyleSheet("background-color: #ffffff")
        self.confirm_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.angle_label = QtWidgets.QLabel(self)
        self.angle_label.setGeometry(QtCore.QRect(20, 20, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.angle_label.setFont(font)

        self.angle_text_edit = QtWidgets.QPlainTextEdit(self)
        self.angle_text_edit.setGeometry(QtCore.QRect(200, 20, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.angle_text_edit.setFont(font)
        self.angle_text_edit.setStyleSheet("background-color: #ffffff")

        self.invalid_label = QtWidgets.QLabel(self)
        self.invalid_label.setGeometry(QtCore.QRect(50, 220, 231, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.invalid_label.setFont(font)
        self.invalid_label.setStyleSheet("")

        self.initial_velocity_label = QtWidgets.QLabel(self)
        self.initial_velocity_label.setGeometry(QtCore.QRect(20, 60, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.initial_velocity_label.setFont(font)

        self.initial_velocity_text_edit = QtWidgets.QPlainTextEdit(self)
        self.initial_velocity_text_edit.setGeometry(QtCore.QRect(200, 60, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.initial_velocity_text_edit.setFont(font)
        self.initial_velocity_text_edit.setStyleSheet("background-color: #ffffff")

        self.positive_direction_image = QtWidgets.QLabel(self)
        self.positive_direction_image.setGeometry(QtCore.QRect(60, 100, 111, 110))
        self.positive_direction_image.setText("")
        self.positive_direction_image.setPixmap(
            QtGui.QPixmap("Images/Simulator/Positive direction.png"))

        self.angle_direction_image = QtWidgets.QLabel(self)
        self.angle_direction_image.setGeometry(QtCore.QRect(170, 100, 81, 61))
        self.angle_direction_image.setText("")
        self.angle_direction_image.setPixmap(QtGui.QPixmap("Images/Simulator/Angle.png"))
        self.angle_direction_image.setScaledContents(True)

        self.angle_label.setText("Angle in degrees:")
        self.initial_velocity_label.setText("Initial velocity:")

        self.__button_actions()

    def __button_actions(self):
        self.confirm_button_box.accepted.connect(self.__save)
        self.confirm_button_box.rejected.connect(self.close)

    def __save(self):
        angle = self.angle_text_edit.toPlainText()
        initial_velocity = self.initial_velocity_text_edit.toPlainText()
        try:
            if len(angle) != 0:
                self.__cannon.rotate_cannon(float(angle))
            if len(initial_velocity) != 0:
                self.__simulation.launch_projectile(self.__projectile, self.__cannon.angle, float(initial_velocity))
            self.close()
        except Exception as e:
            print("Error", e)
            self.invalid_label.setText("Input valid angle and velocity")
