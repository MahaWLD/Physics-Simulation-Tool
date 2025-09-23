from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from database import db, cursor


class Settings(QMainWindow):
    def __init__(self, stack):
        super().__init__(stack)
        self.__WIDTH, self.__HEIGHT = 500, 450
        self.dark_mode = False
        self.show_grid = True
        self.username = None
        self.simulation = None
        self.__stack = stack

        self.__initUI()

        self.tab_widget.setTabEnabled(1, False)     # disable statistics tab if there is no username
        self.fps_slider.setEnabled(False)       # disable when there is no simulation attribute
        self.default_fps_button.setEnabled(False)

    def __initUI(self):
        self.setWindowTitle("Settings")
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: #d1dbe3")

        self.settings_title = QtWidgets.QLabel(self)
        self.settings_title.setGeometry(QtCore.QRect(0, 10, 521, 91))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.settings_title.setFont(font)
        self.settings_title.setStyleSheet("background-color; gray")
        self.settings_title.setAlignment(QtCore.Qt.AlignCenter)

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setGeometry(QtCore.QRect(50, 90, 400, 300))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tab_widget.setFont(font)

        self.tab = QtWidgets.QWidget()

        self.dark_mode_checkbox = QtWidgets.QCheckBox(self.tab)
        self.dark_mode_checkbox.setGeometry(QtCore.QRect(20, 20, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dark_mode_checkbox.setFont(font)

        self.fps_slider = QtWidgets.QSlider(self.tab)
        self.fps_slider.setGeometry(QtCore.QRect(40, 150, 281, 22))
        self.fps_slider.setOrientation(QtCore.Qt.Horizontal)
        self.fps_slider.setMinimum(10)
        self.fps_slider.setMaximum(100)
        self.fps_slider.setValue(60)
        self.fps_slider.setTickInterval(5)

        self.fps_label = QtWidgets.QLabel(self.tab)
        self.fps_label.setGeometry(QtCore.QRect(20, 110, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fps_label.setFont(font)

        self.show_grid_checkbox = QtWidgets.QCheckBox(self.tab)
        self.show_grid_checkbox.setGeometry(QtCore.QRect(20, 55, 121, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.show_grid_checkbox.setFont(font)

        self.default_fps_button = QtWidgets.QPushButton(self.tab)
        self.default_fps_button.setGeometry(QtCore.QRect(20, 190, 121, 23))

        self.tab_widget.addTab(self.tab, "Simulation")

        self.tab_2 = QtWidgets.QWidget()

        self.delete_stats_button = QtWidgets.QPushButton(self.tab_2)
        self.delete_stats_button.setGeometry(QtCore.QRect(70, 227, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.delete_stats_button.setFont(font)
        self.delete_stats_button.setStyleSheet("background-color:rgb(255, 40, 40)")

        self.stats_label = QtWidgets.QLabel(self.tab_2)
        self.stats_label.setGeometry(QtCore.QRect(20, 20, 361, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.stats_label.setFont(font)

        self.questions_answered_label = QtWidgets.QLabel(self.tab_2)
        self.questions_answered_label.setGeometry(QtCore.QRect(40, 60, 321, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.questions_answered_label.setFont(font)

        self.correct_answers_label = QtWidgets.QLabel(self.tab_2)
        self.correct_answers_label.setGeometry(QtCore.QRect(40, 90, 321, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.correct_answers_label.setFont(font)

        self.accuracy_label = QtWidgets.QLabel(self.tab_2)
        self.accuracy_label.setGeometry(QtCore.QRect(40, 120, 321, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.accuracy_label.setFont(font)

        self.tab_widget.addTab(self.tab_2, "Statistics")

        self.settings_title.setText("Settings")
        self.dark_mode_checkbox.setText("Dark mode")
        self.show_grid_checkbox.setText("Show grid")
        self.default_fps_button.setText("Default FPS")
        self.stats_label.setText("Interactive mode question statistics:")
        self.delete_stats_button.setText("Delete statistics")

        if self.simulation:
            self.fps_label.setText(f"FPS: {self.simulation.FPS}")
        else:
            self.fps_label.setText("FPS: 60")

        if self.show_grid:
            self.show_grid_checkbox.setChecked(True)

        self.__button_actions()

    def __button_actions(self):
        self.dark_mode_checkbox.stateChanged.connect(self.__toggle_dark_mode)
        self.show_grid_checkbox.stateChanged.connect(self.__toggle_grid)
        self.delete_stats_button.clicked.connect(self.__delete_stats)
        self.fps_slider.valueChanged.connect(self.__change_fps)
        self.default_fps_button.clicked.connect(self.__set_default_fps)

    def __toggle_grid(self):
        if self.show_grid_checkbox.isChecked():
            self.show_grid = True
        else:
            self.show_grid = False

    def __toggle_dark_mode(self):
        if self.dark_mode_checkbox.isChecked():
            self.dark_mode = True
        else:
            self.dark_mode = False

    def set_username(self, username):
        self.username = username
        self.__show_stats()

        if username != "Guest":
            self.tab_widget.setTabEnabled(1, True)  # enable statistics tab if there is a user which is not a guest

    def set_simulation(self, simulation):
        self.simulation = simulation

        # enable fps settings when simulation scene opened
        self.fps_slider.setEnabled(True)
        self.default_fps_button.setEnabled(True)

    def __show_stats(self):     # aggregate SQL functions

        query = "SELECT COUNT(*) as total_questions FROM Questions"
        cursor.execute(query)
        total_questions = cursor.fetchone()[0]

        query = "SELECT COUNT(*) as answered_questions FROM ProgressTracker " \
                "WHERE userID = %s"
        cursor.execute(query, (self.username,))
        answered_questions = cursor.fetchone()[0]

        self.questions_answered_label.setText(f"Questions answered: {answered_questions}/{total_questions}")

        query = "SELECT SUM(result) as correct_answers FROM ProgressTracker " \
                "WHERE userID = %s"
        cursor.execute(query, (self.username,))
        correct_answers = cursor.fetchone()[0]

        self.correct_answers_label.setText(f"Correct answers: {correct_answers}")

        query = "SELECT AVG(result) as accuracy FROM ProgressTracker " \
                "WHERE userID = %s"
        cursor.execute(query, (self.username,))
        accuracy = cursor.fetchone()[0]

        if accuracy is not None:
            self.accuracy_label.setText(f"Accuracy: {accuracy*100}%")  # x 100 to make it a percentage
        else:
            self.accuracy_label.setText(f"Accuracy: {accuracy}")

    def __delete_stats(self):
        query = "DELETE FROM ProgressTracker " \
                "WHERE userID = %s"
        cursor.execute(query, (self.username,))
        db.commit()
        self.__show_stats()

    def __change_fps(self, value):
        self.fps_label.setText(f"FPS: {value}")
        self.simulation.change_fps(value)

    def __set_default_fps(self):
        self.fps_label.setText("FPS: 60")
        self.fps_slider.setValue(60)
        self.simulation.set_to_default_fps()
