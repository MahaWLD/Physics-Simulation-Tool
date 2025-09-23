from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

from simulation_objects import Cannon


class SceneObjectProperties(QWidget):
    def __init__(self, simulation):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 312, 572
        self.__simulation = simulation
        self.__initIU()
        self.__update_object_combobox()

    def __initIU(self):
        self.setGeometry(100, 100, self.__WIDTH, self.__HEIGHT)
        self.setWindowTitle("Properties")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(21, 19, 275, 151))
        self.groupBox.setStyleSheet("background-color:#7bb2e3")

        self.scene_properties_label = QtWidgets.QLabel(self.groupBox)
        self.scene_properties_label.setGeometry(QtCore.QRect(0, -1, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.scene_properties_label.setFont(font)
        self.scene_properties_label.setAlignment(QtCore.Qt.AlignCenter)

        self.gravitational_acceleration_spinbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.gravitational_acceleration_spinbox.setGeometry(QtCore.QRect(200, 43, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.gravitational_acceleration_spinbox.setFont(font)
        self.gravitational_acceleration_spinbox.setStyleSheet("background-color: #d1dbe3")

        self.gravitational_acceleration_label = QtWidgets.QLabel(self.groupBox)
        self.gravitational_acceleration_label.setGeometry(QtCore.QRect(10, 43, 191, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.gravitational_acceleration_label.setFont(font)

        self.choose_planet_gravitational_acceleration_label = QtWidgets.QLabel(self.groupBox)
        self.choose_planet_gravitational_acceleration_label.setGeometry(QtCore.QRect(10, 68, 221, 16))

        self.earth_gravitational_acceleration_button = QtWidgets.QPushButton(self.groupBox)
        self.earth_gravitational_acceleration_button.setGeometry(QtCore.QRect(22, 94, 51, 31))
        self.earth_gravitational_acceleration_button.setStyleSheet("background-color: rgb(96, 220, 137);")

        self.moon_gravitational_acceleration_button = QtWidgets.QPushButton(self.groupBox)
        self.moon_gravitational_acceleration_button.setGeometry(QtCore.QRect(82, 94, 51, 31))
        self.moon_gravitational_acceleration_button.setStyleSheet("background-color: white")

        self.mars_gravitational_acceleration_button = QtWidgets.QPushButton(self.groupBox)
        self.mars_gravitational_acceleration_button.setGeometry(QtCore.QRect(142, 94, 51, 31))
        self.mars_gravitational_acceleration_button.setStyleSheet("background-color: white")

        self.jupiter_gravitational_acceleration_button = QtWidgets.QPushButton(self.groupBox)
        self.jupiter_gravitational_acceleration_button.setGeometry(QtCore.QRect(202, 94, 51, 31))
        self.jupiter_gravitational_acceleration_button.setStyleSheet("background-color: white")

        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(21, 171, 275, 381))
        self.groupBox_2.setStyleSheet("background-color:#7bb2e3")

        self.object_properties_label = QtWidgets.QLabel(self.groupBox_2)
        self.object_properties_label.setGeometry(QtCore.QRect(0, -1, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.object_properties_label.setFont(font)
        self.object_properties_label.setAlignment(QtCore.Qt.AlignCenter)

        self.mass_spinbox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.mass_spinbox.setGeometry(QtCore.QRect(200, 250, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mass_spinbox.setFont(font)
        self.mass_spinbox.setStyleSheet("background-color: #d1dbe3")

        self.mass_label = QtWidgets.QLabel(self.groupBox_2)
        self.mass_label.setGeometry(QtCore.QRect(19, 252, 161, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mass_label.setFont(font)

        self.object_selected_label = QtWidgets.QLabel(self.groupBox_2)
        self.object_selected_label.setGeometry(QtCore.QRect(19, 50, 161, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.object_selected_label.setFont(font)

        self.object_selected_combobox = QtWidgets.QComboBox(self.groupBox_2)
        self.object_selected_combobox.setGeometry(QtCore.QRect(160, 49, 101, 22))
        self.object_selected_combobox.setStyleSheet("background-color: #d1dbe3")

        self.friction_spinbox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.friction_spinbox.setEnabled(True)
        self.friction_spinbox.setGeometry(QtCore.QRect(200, 310, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.friction_spinbox.setFont(font)
        self.friction_spinbox.setStyleSheet("background-color: #d1dbe3")

        self.elasticity_spinbox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.elasticity_spinbox.setEnabled(True)
        self.elasticity_spinbox.setGeometry(QtCore.QRect(200, 280, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.elasticity_spinbox.setFont(font)
        self.elasticity_spinbox.setStyleSheet("background-color: #d1dbe3")

        self.velocity_vectors_checkbox = QtWidgets.QCheckBox(self.groupBox_2)
        self.velocity_vectors_checkbox.setGeometry(QtCore.QRect(19, 114, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.velocity_vectors_checkbox.setFont(font)

        self.elasticity_label = QtWidgets.QLabel(self.groupBox_2)
        self.elasticity_label.setGeometry(QtCore.QRect(20, 282, 161, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.elasticity_label.setFont(font)

        self.friction_label = QtWidgets.QLabel(self.groupBox_2)
        self.friction_label.setGeometry(QtCore.QRect(20, 314, 161, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.friction_label.setFont(font)

        self.update_list_button = QtWidgets.QPushButton(self.groupBox_2)
        self.update_list_button.setGeometry(QtCore.QRect(20, 80, 111, 23))
        self.update_list_button.setStyleSheet("background-color:rgb(111, 212, 255)")

        self.delete_object_button = QtWidgets.QPushButton(self.groupBox_2)
        self.delete_object_button.setGeometry(QtCore.QRect(30, 340, 221, 23))
        self.delete_object_button.setStyleSheet("background-color:rgb(255, 40, 40)")

        self.confirm_edits_button = QtWidgets.QPushButton(self.groupBox_2)
        self.confirm_edits_button.setGeometry(QtCore.QRect(145, 80, 110, 23))
        self.confirm_edits_button.setStyleSheet("background-color:rgb(111, 212, 255)")

        self.force_vectors_checkbox = QtWidgets.QCheckBox(self.groupBox_2)
        self.force_vectors_checkbox.setGeometry(QtCore.QRect(20, 145, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.force_vectors_checkbox.setFont(font)

        self.apply_force_button = QtWidgets.QPushButton(self.groupBox_2)
        self.apply_force_button.setGeometry(QtCore.QRect(40, 179, 201, 23))
        self.apply_force_button.setStyleSheet("background-color:rgb(111, 212, 255)")

        self.remove_all_forces_button = QtWidgets.QPushButton(self.groupBox_2)
        self.remove_all_forces_button.setGeometry(QtCore.QRect(40, 211, 201, 23))
        self.remove_all_forces_button.setStyleSheet("background-color:rgb(111, 212, 255)")

        self.scene_properties_label.setText("Scene properties")
        self.gravitational_acceleration_label.setText("Gravitational acceleration:")
        self.earth_gravitational_acceleration_button.setText("Earth")
        self.moon_gravitational_acceleration_button.setText("Moon")
        self.mars_gravitational_acceleration_button.setText("Mars")
        self.jupiter_gravitational_acceleration_button.setText("Jupiter")
        self.object_properties_label.setText("Object properties")
        self.mass_label.setText("Mass:")
        self.object_selected_label.setText("Object selected:")
        self.velocity_vectors_checkbox.setText("Velocity vectors")
        self.force_vectors_checkbox.setText("Force vectors")
        self.apply_force_button.setText("Apply force")
        self.remove_all_forces_button.setText("Remove all forces")
        self.elasticity_label.setText("Elasticity:")
        self.friction_label.setText("Friction:")
        self.update_list_button.setText("Update list")
        self.confirm_edits_button.setText("Confirm edits")
        self.delete_object_button.setText("Delete object")

        self.gravitational_acceleration_spinbox.setValue(self.__simulation.get_gravitational_acceleration("Earth"))

        self.__button_actions()

    def __button_actions(self):
        self.earth_gravitational_acceleration_button.clicked.connect(self.__edit_gravitational_acceleration)
        self.moon_gravitational_acceleration_button.clicked.connect(self.__edit_gravitational_acceleration)
        self.mars_gravitational_acceleration_button.clicked.connect(self.__edit_gravitational_acceleration)
        self.jupiter_gravitational_acceleration_button.clicked.connect(self.__edit_gravitational_acceleration)

        self.object_selected_combobox.currentIndexChanged.connect(self.__display_properties)
        self.update_list_button.clicked.connect(self.__update_object_combobox)
        self.confirm_edits_button.clicked.connect(self.__edit_properties)
        self.apply_force_button.clicked.connect(self.__show_apply_force_window)
        self.remove_all_forces_button.clicked.connect(self.__remove_all_forces)
        self.delete_object_button.clicked.connect(self.__delete_object_selected)

        self.gravitational_acceleration_spinbox.textChanged.connect(self.__edit_properties)

    def __edit_gravitational_acceleration(self):
        button = self.sender()

        buttons = [
            self.earth_gravitational_acceleration_button,
            self.moon_gravitational_acceleration_button,
            self.mars_gravitational_acceleration_button,
            self.jupiter_gravitational_acceleration_button
        ]

        for i in buttons:
            if button == i:
                i.setStyleSheet("background-color: rgb(96, 220, 137);")
            else:
                i.setStyleSheet("background-color: white")

        if button == self.earth_gravitational_acceleration_button:
            self.gravitational_acceleration_spinbox.setValue(self.__simulation.get_gravitational_acceleration("Earth"))
            self.__simulation.edit_gravitational_acceleration(self.__simulation.get_gravitational_acceleration("Earth"))
        elif button == self.moon_gravitational_acceleration_button:
            self.gravitational_acceleration_spinbox.setValue(self.__simulation.get_gravitational_acceleration("Moon"))
            self.__simulation.edit_gravitational_acceleration(self.__simulation.get_gravitational_acceleration("Moon"))
        elif button == self.mars_gravitational_acceleration_button:
            self.gravitational_acceleration_spinbox.setValue(self.__simulation.get_gravitational_acceleration("Mars"))
            self.__simulation.edit_gravitational_acceleration(self.__simulation.get_gravitational_acceleration("Mars"))
        else:
            self.gravitational_acceleration_spinbox.setValue(
                self.__simulation.get_gravitational_acceleration("Jupiter"))
            self.__simulation.edit_gravitational_acceleration(
                self.__simulation.get_gravitational_acceleration("Jupiter"))

    def __find_object_selected(self):  # linear search
        obj_name = self.object_selected_combobox.currentText()
        items = self.__simulation.objects + self.__simulation.models
        for obj in items:
            if obj_name == obj.name:
                object_selected = obj
                return object_selected

    def __display_properties(self):
        obj = self.__find_object_selected()

        if hasattr(obj, "show_velocity_vectors"):
            if obj.show_velocity_vectors:
                self.velocity_vectors_checkbox.setChecked(True)
        if hasattr(obj, "show_force_vectors"):
            if obj.show_force_vectors:
                self.force_vectors_checkbox.setChecked(True)

        self.velocity_vectors_checkbox.stateChanged.connect(self.__show_hide_velocity_vectors)
        self.force_vectors_checkbox.stateChanged.connect(self.__show_hide_force_vectors)

        if hasattr(obj, "mass"):
            self.mass_spinbox.setValue(obj.shape.mass)
        else:
            self.mass_spinbox.setValue(0)

        if isinstance(obj, Cannon):
            self.elasticity_spinbox.setValue(0)
            self.friction_spinbox.setValue(0)
        else:
            if hasattr(obj, "elasticity"):
                self.elasticity_spinbox.setValue(obj.shape.elasticity)
            else:
                self.elasticity_spinbox.setValue(0)
            if hasattr(obj, "friction"):
                self.friction_spinbox.setValue(obj.shape.friction)
            else:
                self.friction_spinbox.setValue(0)

        if obj in self.__simulation.objects:
            self.apply_force_button.setEnabled(True)
            self.remove_all_forces_button.setEnabled(True)
            self.delete_object_button.setEnabled(True)
            self.velocity_vectors_checkbox.setEnabled(True)
            self.force_vectors_checkbox.setEnabled(True)
        else:
            self.apply_force_button.setEnabled(False)
            self.remove_all_forces_button.setEnabled(False)
            self.delete_object_button.setEnabled(False)
            self.velocity_vectors_checkbox.setEnabled(False)
            self.force_vectors_checkbox.setEnabled(False)

    def __edit_properties(self):
        print("[Editing properties]")
        gravitational_acceleration = self.gravitational_acceleration_spinbox.value()
        self.__simulation.edit_gravitational_acceleration(gravitational_acceleration)

        obj = self.__find_object_selected()
        properties_data = {
            "mass": float(self.mass_spinbox.value()),
            "elasticity": float(self.elasticity_spinbox.value()),
            "friction": float(self.friction_spinbox.value())
        }
        self.__simulation.edit_object_properties(obj, properties_data)
        self.__display_properties()

    def __update_object_combobox(self):
        self.object_selected_combobox.clear()

        for obj in self.__simulation.objects:
            self.object_selected_combobox.addItem(obj.name)

        for obj in self.__simulation.models:
            self.object_selected_combobox.addItem(obj.name)

    def __delete_object_selected(self):
        object_selected = self.__find_object_selected()
        self.__simulation.delete_object(object_selected, True)

    def __show_hide_velocity_vectors(self):
        obj = self.__find_object_selected()
        obj.toggle_velocity_vectors()

    def __show_hide_force_vectors(self):
        obj = self.__find_object_selected()
        obj.toggle_force_vectors()

    def __show_apply_force_window(self):
        obj = self.__find_object_selected()
        self.apply_force_window = ForceInput(self.__simulation, obj)
        self.apply_force_window.show()

    def __remove_all_forces(self):
        obj = self.__find_object_selected()
        obj.force_x = 0
        obj.force_y = 0


class ForceInput(QWidget):
    def __init__(self, simulation, obj):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 425, 174
        self.__simulation = simulation
        self.__object = obj
        self.__initUI()

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setWindowTitle("Apply force")
        self.setStyleSheet("background-color: #d1dbe3")

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(13, 50, 401, 111))

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

        self.positive_direction_image = QtWidgets.QLabel(self.tab)
        self.positive_direction_image.setGeometry(QtCore.QRect(110, 20, 71, 71))
        self.positive_direction_image.setText("")
        self.positive_direction_image.setPixmap(QtGui.QPixmap("Images/Simulator/Positive direction.png"))
        self.positive_direction_image.setScaledContents(True)

        self.tabWidget.addTab(self.tab, "Horizontal and vertical")

        self.tab_2 = QtWidgets.QWidget()

        self.force_label = QtWidgets.QLabel(self.tab_2)
        self.force_label.setGeometry(QtCore.QRect(18, 20, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.force_label.setFont(font)

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

        self.force_text_edit = QtWidgets.QPlainTextEdit(self.tab_2)
        self.force_text_edit.setGeometry(QtCore.QRect(195, 8, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.force_text_edit.setFont(font)
        self.force_text_edit.setStyleSheet("background-color: white")

        self.angle_image = QtWidgets.QLabel(self.tab_2)
        self.angle_image.setGeometry(QtCore.QRect(80, 20, 91, 51))
        self.angle_image.setText("")
        self.angle_image.setPixmap(QtGui.QPixmap("Images/Simulator/Angle.png"))
        self.angle_image.setScaledContents(True)

        self.tabWidget.addTab(self.tab_2, "At an angle")

        self.apply_force_label = QtWidgets.QLabel(self)
        self.apply_force_label.setGeometry(QtCore.QRect(10, 18, 411, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.apply_force_label.setFont(font)
        self.apply_force_label.setAlignment(QtCore.Qt.AlignCenter)

        self.apply_force_label.setText("Apply force")
        self.x_label.setText("Horizontal:")
        self.y_label.setText("Vertical:")
        self.done_button.setText("Done")
        self.force_label.setText("Force:")
        self.angle_label.setText("Angle:")
        self.done_button_2.setText("Done")

        self.__button_actions()

    def __button_actions(self):
        self.done_button.clicked.connect(self.__collect_data)
        self.done_button_2.clicked.connect(self.__collect_data)

    def __collect_data(self):
        self.close()
        button = self.sender()
        force_data = {"object": self.__object}

        if button == self.done_button:
            force_x = self.x_text_edit.toPlainText()
            force_y = self.y_text_edit.toPlainText()
            if force_x == "":
                force_x = 0
            if force_y == "":
                force_y = 0
            try:
                force_data["force_x"] = float(force_x)
                force_data["force_y"] = float(force_y)
                self.__simulation.apply_force_to_object(self.__object, force_data, resolved=True)
            except Exception as e:  # if something invalid is inputted
                print("Error", e)
        else:
            force = self.force_text_edit.toPlainText()
            angle = self.angle_text_edit.toPlainText()
            if force == "":
                force = 0
            if angle == "":
                angle = 0
            try:
                force_data["force"] = float(force)
                force_data["angle"] = float(angle)
                self.__simulation.apply_force_to_object(self.__object, force_data, resolved=False)
            except Exception as e:
                print("Error", e)
