from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class ObjectTab(QWidget):
    def __init__(self, simulation):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 750, 200
        self.__simulation = simulation
        self.__initUI()

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #b4cede")
        self.setGeometry(550, 750, self.__WIDTH, self.__HEIGHT)
        self.setWindowTitle("Object Tab")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)

        self.tabWidget = QtWidgets.QTabWidget(self)

        self.tab = QtWidgets.QWidget()

        self.scrollArea = QtWidgets.QScrollArea(self.tab)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 710, 130))
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setEnabled(True)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 708, 128))

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)

        self.object_button1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.object_button1.setStyleSheet("background-color: #d1dbe3")

        self.horizontalLayout_2.addWidget(self.object_button1)

        self.object_button2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.object_button2.setStyleSheet("background-color: #d1dbe3")

        self.horizontalLayout_2.addWidget(self.object_button2)

        self.object_button3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.object_button3.setStyleSheet("background-color: #d1dbe3")

        self.horizontalLayout_2.addWidget(self.object_button3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()

        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 10, 710, 130))
        self.scrollArea_2.setWidgetResizable(True)

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setEnabled(True)
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 708, 128))

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)

        self.model1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.model1.setStyleSheet("background-color: #d1dbe3")

        self.horizontalLayout_3.addWidget(self.model1)

        self.model2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.model2.setStyleSheet("background-color: #d1dbe3")

        self.horizontalLayout_3.addWidget(self.model2)

        self.model3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.model3.setStyleSheet("background-color: #d1dbe3")

        self.horizontalLayout_3.addWidget(self.model3)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        self.object_button1.setText("Ball")
        self.object_button2.setText("Block")
        self.object_button3.setText("")

        self.model1.setText("Cannon")
        self.model2.setText("")
        self.model3.setText("")

        self.tabWidget.setTabText(0, "Objects")
        self.tabWidget.setTabText(1, "Prebuilt Models")

        self.__button_actions()

    def __button_actions(self):
        self.object_button1.clicked.connect(lambda: self.__open_add_object("ball"))
        self.object_button2.clicked.connect(lambda: self.__open_add_object("block"))
        self.model1.clicked.connect(self.__add_cannon)

    def __open_add_object(self, item):
        self.add_object_window = AddObjectWindow(item, self.__simulation)
        self.add_object_window.show()
        self.close()

    def __add_cannon(self):
        self.close()
        position_x = self.__simulation.get_mouse_position()[0]
        self.__simulation.add_cannon(position_x)


class AddObjectWindow(QWidget):
    def __init__(self, obj, simulation):
        super().__init__()
        self.__object = obj
        self.__simulation = simulation
        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("Add object")
        if self.__object == "ball":
            self.radius_label = QtWidgets.QLabel(self)
            self.radius_label.setGeometry(QtCore.QRect(30, 140, 71, 21))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.radius_label.setFont(font)

            self.radius_text_edit = QtWidgets.QPlainTextEdit(self)
            self.radius_text_edit.setGeometry(QtCore.QRect(115, 136, 51, 30))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.radius_text_edit.setFont(font)
            self.radius_text_edit.setStyleSheet("background-color: white")

            self.radius_label.setText("Radius:")
            self.radius_text_edit.setPlainText("1")

        elif self.__object == "block":
            self.width_label = QtWidgets.QLabel(self)
            self.width_label.setGeometry(QtCore.QRect(30, 140, 71, 21))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.width_label.setFont(font)

            self.width_text_edit = QtWidgets.QPlainTextEdit(self)
            self.width_text_edit.setGeometry(QtCore.QRect(115, 136, 51, 30))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.width_text_edit.setFont(font)
            self.width_text_edit.setStyleSheet("background-color: white")

            self.height_label = QtWidgets.QLabel(self)
            self.height_label.setGeometry(QtCore.QRect(30, 179, 71, 21))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.height_label.setFont(font)

            self.height_text_edit = QtWidgets.QPlainTextEdit(self)
            self.height_text_edit.setGeometry(QtCore.QRect(115, 175, 51, 30))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.height_text_edit.setFont(font)
            self.height_text_edit.setStyleSheet("background-color: white")

            self.width_label.setText("Width:")
            self.height_label.setText("Height:")

            self.width_text_edit.setPlainText("1")
            self.height_text_edit.setPlainText("1")

        self.mass_label = QtWidgets.QLabel(self)
        self.mass_label.setGeometry(QtCore.QRect(30, 100, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mass_label.setFont(font)

        self.velocity_label = QtWidgets.QLabel(self)
        self.velocity_label.setGeometry(QtCore.QRect(30, 234, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.velocity_label.setFont(font)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(30, 274, 401, 111))

        self.tab = QtWidgets.QWidget()

        self.x_label = QtWidgets.QLabel(self.tab)
        self.x_label.setGeometry(QtCore.QRect(18, 20, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.x_label.setFont(font)

        self.y_label = QtWidgets.QLabel(self.tab)
        self.y_label.setGeometry(QtCore.QRect(18, 50, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.y_label.setFont(font)

        self.done_button = QtWidgets.QPushButton(self.tab)
        self.done_button.setGeometry(QtCore.QRect(270, 20, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.done_button.setFont(font)
        self.done_button.setStyleSheet("background-color: rgb(96, 220, 137);")

        self.y_text_edit = QtWidgets.QPlainTextEdit(self.tab)
        self.y_text_edit.setGeometry(QtCore.QRect(195, 46, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.y_text_edit.setFont(font)
        self.y_text_edit.setStyleSheet("background-color: white")

        self.x_text_edit = QtWidgets.QPlainTextEdit(self.tab)
        self.x_text_edit.setGeometry(QtCore.QRect(195, 8, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.x_text_edit.setFont(font)
        self.x_text_edit.setStyleSheet("background-color: white")

        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()

        self.velocity_label_2 = QtWidgets.QLabel(self.tab_2)
        self.velocity_label_2.setGeometry(QtCore.QRect(18, 20, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.velocity_label_2.setFont(font)

        self.angle_label = QtWidgets.QLabel(self.tab_2)
        self.angle_label.setGeometry(QtCore.QRect(18, 50, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.angle_label.setFont(font)

        self.done_button_2 = QtWidgets.QPushButton(self.tab_2)
        self.done_button_2.setGeometry(QtCore.QRect(270, 20, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.done_button_2.setFont(font)
        self.done_button_2.setStyleSheet("background-color: rgb(96, 220, 137);")

        self.angle_text_edit = QtWidgets.QPlainTextEdit(self.tab_2)
        self.angle_text_edit.setGeometry(QtCore.QRect(195, 46, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.angle_text_edit.setFont(font)
        self.angle_text_edit.setStyleSheet("background-color: white")

        self.velocity_text_edit = QtWidgets.QPlainTextEdit(self.tab_2)
        self.velocity_text_edit.setGeometry(QtCore.QRect(195, 8, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.velocity_text_edit.setFont(font)
        self.velocity_text_edit.setStyleSheet("background-color: white")

        self.angle_image = QtWidgets.QLabel(self.tab_2)
        self.angle_image.setGeometry(QtCore.QRect(80, 20, 91, 51))
        self.angle_image.setText("")
        self.angle_image.setPixmap(QtGui.QPixmap("Images/Simulator/Angle.png"))
        self.angle_image.setScaledContents(True)

        self.tabWidget.addTab(self.tab_2, "")

        self.add_object_label = QtWidgets.QLabel(self)
        self.add_object_label.setGeometry(QtCore.QRect(10, 20, 451, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.add_object_label.setFont(font)
        self.add_object_label.setAlignment(QtCore.Qt.AlignCenter)

        self.mass_text_edit = QtWidgets.QPlainTextEdit(self)
        self.mass_text_edit.setGeometry(QtCore.QRect(115, 98, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mass_text_edit.setFont(font)
        self.mass_text_edit.setStyleSheet("background-color: white")

        self.elasticity_text_edit = QtWidgets.QPlainTextEdit(self)
        self.elasticity_text_edit.setGeometry(QtCore.QRect(306, 98, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.elasticity_text_edit.setFont(font)
        self.elasticity_text_edit.setStyleSheet("background-color: white")

        self.elasticity_label = QtWidgets.QLabel(self)
        self.elasticity_label.setGeometry(QtCore.QRect(222, 99, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.elasticity_label.setFont(font)

        self.friction_text_edit = QtWidgets.QPlainTextEdit(self)
        self.friction_text_edit.setGeometry(QtCore.QRect(306, 136, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.friction_text_edit.setFont(font)
        self.friction_text_edit.setStyleSheet("background-color: white")

        self.friction_label = QtWidgets.QLabel(self)
        self.friction_label.setGeometry(QtCore.QRect(222, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.friction_label.setFont(font)

        self.mass_label.setText("Mass:")
        self.elasticity_label.setText("Elasticity:")
        self.friction_label.setText("Friction:")
        self.velocity_label.setText("Velocity:")
        self.x_label.setText("Horizontal:")
        self.y_label.setText("Vertical:")
        self.done_button.setText("Done")
        self.velocity_label_2.setText("Velocity:")
        self.angle_label.setText("Angle:")
        self.done_button_2.setText("Done")
        self.add_object_label.setText("Add " + str(self.__object))

        self.mass_text_edit.setPlainText("50")
        self.elasticity_text_edit.setPlainText("0.5")
        self.friction_text_edit.setPlainText("0.5")
        self.x_text_edit.setPlainText("0")
        self.y_text_edit.setPlainText("0")
        self.velocity_text_edit.setPlainText("0")
        self.angle_text_edit.setPlainText("0")

        self.tabWidget.setTabText(0, "Horizontal and vertical")
        self.tabWidget.setTabText(1, "At an angle")

        self.__button_actions()

    def __button_actions(self):
        self.done_button.clicked.connect(self.__collect_data)
        self.done_button_2.clicked.connect(self.__collect_data)

    def __collect_data(self):
        try:
            self.close()
            button = self.sender()
            position = self.__simulation.get_mouse_position()

            mass = float(self.mass_text_edit.toPlainText())
            elasticity = float(self.elasticity_text_edit.toPlainText())
            friction = float(self.friction_text_edit.toPlainText())

            if mass <= 0:
                raise ValueError("Mass must be greater than 0")

            if elasticity < 0 or elasticity > 1:
                raise ValueError("Elasticity must be between 0 and 1")

            if friction < 0:
                raise ValueError("Friction must be greater than or equal to 0")

            data = {
                "object": self.__object,
                "mass": mass,
                "elasticity": elasticity,
                "friction": friction,
                "position": position
            }

            if self.__object == "ball":
                radius = float(self.radius_text_edit.toPlainText())
                if radius <= 0:
                    raise ValueError("Radius must be greater than 0")
                data["radius"] = radius
            else:
                width = float(self.width_text_edit.toPlainText())
                height = float(self.height_text_edit.toPlainText())
                if width <= 0 or height <= 0:
                    raise ValueError("Width and height must be greater than 0")
                data["width"] = width
                data["height"] = height

            if button == self.done_button:
                initial_velocity_x = float(self.x_text_edit.toPlainText())
                initial_velocity_y = float(self.y_text_edit.toPlainText())
                data["initial_velocity_x"] = initial_velocity_x
                data["initial_velocity_y"] = initial_velocity_y
                self.__simulation.add_object(data, resolved=True)
            else:
                initial_velocity = float(self.velocity_text_edit.toPlainText())
                velocity_angle = float(self.angle_text_edit.toPlainText())
                data["initial_velocity"] = initial_velocity
                data["velocity_angle"] = velocity_angle
                self.__simulation.add_object(data, resolved=False)
        except ValueError as ve:
            print("Error", f"Invalid input: {ve}")
        except Exception as e:
            print("Error", str(e))
