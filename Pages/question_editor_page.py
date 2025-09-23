from Pages.page import Page
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from SimulationTabs.InteractiveMode.question_tree import QuestionTree

from database import db, cursor


class QuestionEditorPage(Page):
    def __init__(self, stack):
        super().__init__()
        self.__stack = stack
        self.question_tree = QuestionTree.load_tree("question_tree.bin")    # get question tree
        self.__initUI()
        self.__populate_tree_widget()

    def __initUI(self):
        super()._initUI()
        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setGeometry(QtCore.QRect(80, 260, 1151, 481))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.treeWidget.setFont(font)

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

        self.add_question_button = QtWidgets.QPushButton(self)
        self.add_question_button.setGeometry(QtCore.QRect(1290, 400, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.add_question_button.setFont(font)

        self.add_model_button = QtWidgets.QPushButton(self)
        self.add_model_button.setGeometry(QtCore.QRect(1290, 470, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.add_model_button.setFont(font)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(75, 50, 75, 75))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/BackButtonIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_button.setIcon(icon)
        self.back_button.setIconSize(QtCore.QSize(60, 60))

        self.refresh_button = QtWidgets.QPushButton(self)
        self.refresh_button.setGeometry(QtCore.QRect(760, 810, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.refresh_button.setFont(font)

        self.title.setText("Question Editor")
        self.add_question_button.setText("Add question")
        self.add_model_button.setText("Add model")
        self.refresh_button.setText("Refresh")

        self.__button_actions()

    def __populate_tree_widget(self):
        self.treeWidget.clear()

        for model_node in self.question_tree.root.children:
            # add each model
            model_item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            model_item.setText(0, model_node.data)

            for difficulty_node in model_node.children:
                # set each difficulty under each model
                difficulty_item = QtWidgets.QTreeWidgetItem(model_item)
                difficulty_item.setText(0, difficulty_node.data)

                for question_node in difficulty_node.children:
                    # set each question under each difficulty
                    question_item = QtWidgets.QTreeWidgetItem(difficulty_item)
                    question_item.setText(0, question_node.data)
                    question_item.setText(1, str(question_node.answer))
                    question_item.setFlags(question_item.flags() & ~QtCore.Qt.ItemIsUserCheckable)

    def __button_actions(self):
        self.add_question_button.clicked.connect(self.__open_choose_question_input)
        self.add_model_button.clicked.connect(self.__open_add_model)
        self.back_button.clicked.connect(lambda: self.__stack.setCurrentIndex(1))
        self.refresh_button.clicked.connect(self.__populate_tree_widget)

    def __open_choose_question_input(self):
        self.choose_question_window = ChooseQuestionInput(self.question_tree)
        self.choose_question_window.show()

    def __open_add_model(self):
        self.add_model_window = ModelInput(self.question_tree)
        self.add_model_window.show()


class ChooseQuestionInput(QWidget):
    def __init__(self, question_tree):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 460, 212
        self.question_tree = question_tree
        self.__initUI()

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #d1dbe3")
        self.setGeometry(550, 750, self.__WIDTH, self.__HEIGHT)
        self.setWindowTitle("Choose Question Input")

        self.model_label = QtWidgets.QLabel(self)
        self.model_label.setGeometry(QtCore.QRect(40, 30, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.model_label.setFont(font)

        self.difficulty_level_label = QtWidgets.QLabel(self)
        self.difficulty_level_label.setGeometry(QtCore.QRect(40, 70, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.difficulty_level_label.setFont(font)

        self.question_button = QtWidgets.QPushButton(self)
        self.question_button.setGeometry(QtCore.QRect(140, 130, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.question_button.setFont(font)
        self.question_button.setStyleSheet("background-color: #ffffff")

        self.difficulty_level_combobox = QtWidgets.QComboBox(self)
        self.difficulty_level_combobox.setGeometry(QtCore.QRect(220, 70, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.difficulty_level_combobox.setFont(font)
        self.difficulty_level_combobox.setStyleSheet("background-color: #ffffff")

        self.difficulty_level_combobox.addItem("Easy")
        self.difficulty_level_combobox.addItem("Intermediate")
        self.difficulty_level_combobox.addItem("Difficult")

        self.model_selected_combobox = QtWidgets.QComboBox(self)
        self.model_selected_combobox.setGeometry(QtCore.QRect(220, 30, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.model_selected_combobox.setFont(font)
        self.model_selected_combobox.setStyleSheet("background-color: #ffffff")

        model_nodes = self.question_tree.get_model_nodes()
        for model in model_nodes:
            self.model_selected_combobox.addItem(model.data)

        self.model_label.setText("Model:")
        self.difficulty_level_label.setText("Difficulty level:")
        self.question_button.setText("Add a question")

        self.__button_actions()

    def __button_actions(self):
        self.question_button.clicked.connect(self.__open_question_input)

    def __open_question_input(self):
        model = self.model_selected_combobox.currentText()
        difficulty_level = self.difficulty_level_combobox.currentText()
        self.question_input = QuestionInput(self.question_tree, model, difficulty_level)
        self.question_input.show()
        self.close()


class QuestionInput(QWidget):
    def __init__(self, question_tree, model, difficulty_level):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 966, 212
        self.question_tree = question_tree
        self.model = model
        self.difficulty_level = difficulty_level
        self.__initUI()

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #d1dbe3")
        self.setWindowTitle("Question Input")

        self.question_label = QtWidgets.QLabel(self)
        self.question_label.setGeometry(QtCore.QRect(50, 20, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.question_label.setFont(font)

        self.add_question_button = QtWidgets.QPushButton(self)
        self.add_question_button.setGeometry(QtCore.QRect(410, 140, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_question_button.setFont(font)
        self.add_question_button.setStyleSheet("background-color: #ffffff")

        self.question_text_edit = QtWidgets.QLineEdit(self)
        self.question_text_edit.setGeometry(QtCore.QRect(190, 20, 751, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.question_text_edit.setFont(font)
        self.question_text_edit.setStyleSheet("background-color: #ffffff")

        self.answer_text_edit = QtWidgets.QLineEdit(self)
        self.answer_text_edit.setGeometry(QtCore.QRect(190, 70, 751, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.answer_text_edit.setFont(font)
        self.answer_text_edit.setStyleSheet("background-color: #ffffff")

        self.answer_label = QtWidgets.QLabel(self)
        self.answer_label.setGeometry(QtCore.QRect(50, 70, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.answer_label.setFont(font)

        self.invalid_label = QtWidgets.QLabel(self)
        self.invalid_label.setGeometry(QtCore.QRect(90, 140, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.invalid_label.setFont(font)

        self.question_label.setText("Question:")
        self.answer_label.setText("Answer:")
        self.add_question_button.setText("Add question")

        self.__button_actions()

    def __button_actions(self):
        self.add_question_button.clicked.connect(self.__add_question)

    def __add_question(self):
        question = self.question_text_edit.text()
        answer = self.answer_text_edit.text()

        if question != "" and answer != "":

            self.question_tree.add_question(self.model, self.difficulty_level, question, answer)    # add question node
            self.question_tree.save_tree("question_tree.bin")   # update file

            # add record in question table
            insert_question_query = '''
                        INSERT INTO Questions(model, difficulty_level, question, correct_answer)
                        VALUES (%s, %s, %s, %s)'''

            cursor.execute(insert_question_query, (self.model, self.difficulty_level, question, answer))
            db.commit()

            self.close()

        else:
            self.invalid_label.setText("Input valid question and answer")


class ModelInput(QWidget):
    def __init__(self, question_tree):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 626, 145
        self.question_tree = question_tree
        self.__initUI()

    def __initUI(self):
        self.resize(self.__WIDTH, self.__HEIGHT)
        self.setStyleSheet("background-color: #d1dbe3")
        self.setWindowTitle("Model Input")

        self.model_label = QtWidgets.QLabel(self)
        self.model_label.setGeometry(QtCore.QRect(50, 20, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.model_label.setFont(font)

        self.add_model_button = QtWidgets.QPushButton(self)
        self.add_model_button.setGeometry(QtCore.QRect(220, 80, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_model_button.setFont(font)
        self.add_model_button.setStyleSheet("background-color: #ffffff")

        self.model_text_edit = QtWidgets.QLineEdit(self)
        self.model_text_edit.setGeometry(QtCore.QRect(190, 20, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.model_text_edit.setFont(font)
        self.model_text_edit.setStyleSheet("background-color: #ffffff")

        self.invalid_label = QtWidgets.QLabel(self)
        self.invalid_label.setGeometry(QtCore.QRect(60, 80, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.invalid_label.setFont(font)

        self.model_label.setText("Model:")
        self.add_model_button.setText("Add model")

        self.__button_actions()

    def __button_actions(self):
        self.add_model_button.clicked.connect(self.__add_model)

    def __add_model(self):
        model = self.model_text_edit.text()
        if model:
            self.question_tree.add_model(model)
            self.close()
        else:
            self.invalid_label.setText("Input valid model")
