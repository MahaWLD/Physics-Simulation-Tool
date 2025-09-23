from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

from SimulationTabs.InteractiveMode.question_tree import QuestionTree

from database import cursor, db


class InteractiveMode(QWidget):
    def __init__(self, simulation, username):
        super().__init__()
        self.__WIDTH, self.__HEIGHT = 1200, 212
        self.__simulation = simulation
        self.__username = username
        self.question_tree = QuestionTree()
        self.current_model = "Projectile"
        self.current_difficulty = "Easy"
        self.question_node = None
        self.current_index = 0

        self.preset_questions_data = {
            "Projectile": {
                "Easy": {"True or false? The motion of the projectile is dependent on the mass of it.": "false",
                         "True or false? The distance the projectile travels is dependent on the angle of projection.":
                             "true"},
                "Intermediate": {
                    "If the projectile is launched with a velocity of 50 m/s, with an angle of 30° to the positive "
                    "horizontal, what would the vertical velocity component be in m/s?": 25,
                    "If the projectile is launched with a velocity of 15 m/s, with an angle of 60° to the positive "
                    "horizontal, what would the horizontal velocity component be in m/s?": 7.5},
                "Difficult": {
                    "The projectile is launched with a velocity of 15 m/s with an angle of 80° to the positive "
                    "horizontal, what is the maximum height it reaches in m to 2 d.p.?": 11.12,
                    "The projectile is launched with a velocity of 10 m/s with an angle of 60° to the positive "
                    "horizontal, what is its range of flight in m to 2 d.p.?": 8.49
                }
            }
        }

        # load the question tree from the file
        self.question_tree = QuestionTree.load_tree("question_tree.bin")
        if self.question_tree.root is None:
            # build the question tree if it is not loaded from the file
            self.question_tree.build_question_tree(self.preset_questions_data)
            # save the question tree to a file
            self.question_tree.save_tree("question_tree.bin")

        # self.__insert_preset_questions()  # run once to insert preset questions into the database
        self.__initUI()
        self.__display_question(self.current_model, self.current_difficulty)

    def __initUI(self):
        self.setGeometry(300, 800, self.__WIDTH, self.__HEIGHT)
        self.setWindowTitle("Interactive Mode")
        self.setStyleSheet("background-color: #d1dbe3")

        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(QtCore.QRect(0, 20, 1201, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.question_label = QtWidgets.QLabel(self)
        self.question_label.setGeometry(QtCore.QRect(0, 60, 1201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.question_label.setFont(font)
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)

        self.answer_text_edit = QtWidgets.QLineEdit(self)
        self.answer_text_edit.setGeometry(QtCore.QRect(460, 107, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.answer_text_edit.setFont(font)
        self.answer_text_edit.setStyleSheet("background-color: #ffffff")

        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.setGeometry(QtCore.QRect(500, 164, 91, 23))
        self.submit_button.setStyleSheet("background-color: rgb(96, 220, 137);")

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.setGeometry(QtCore.QRect(605, 164, 91, 23))
        self.next_button.setStyleSheet("background-color: #ffffff")

        self.easy_button = QtWidgets.QPushButton(self)
        self.easy_button.setGeometry(QtCore.QRect(830, 20, 81, 23))
        self.easy_button.setStyleSheet("background-color: #9ba2a8")

        self.intermediate_button = QtWidgets.QPushButton(self)
        self.intermediate_button.setGeometry(QtCore.QRect(910, 20, 81, 23))
        self.intermediate_button.setStyleSheet("background-color: #ffffff")

        self.difficult_button = QtWidgets.QPushButton(self)
        self.difficult_button.setGeometry(QtCore.QRect(990, 20, 81, 23))
        self.difficult_button.setStyleSheet("background-color: #ffffff")

        self.result_label = QtWidgets.QLabel(self)
        self.result_label.setGeometry(QtCore.QRect(770, 120, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.result_label.setFont(font)

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(190, 26, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: #ffffff")
        self.comboBox.addItem("Projectile")
        self.comboBox.addItem("Other")

        self.title.setText(f"{self.current_model} Questions")
        self.easy_button.setText("Easy")
        self.intermediate_button.setText("Intermediate")
        self.difficult_button.setText("Difficult")
        self.submit_button.setText("Submit")
        self.next_button.setText("Next question")

        self.__button_actions()

    def __button_actions(self):
        self.easy_button.clicked.connect(self.__edit_question_difficulty)
        self.intermediate_button.clicked.connect(self.__edit_question_difficulty)
        self.difficult_button.clicked.connect(self.__edit_question_difficulty)

        self.comboBox.currentIndexChanged.connect(self.__edit_model)

        self.submit_button.clicked.connect(self.__submit_question)
        self.next_button.clicked.connect(self.__next_question)

    def __edit_question_difficulty(self):
        button = self.sender()

        buttons = [
            self.easy_button,
            self.intermediate_button,
            self.difficult_button
        ]

        # highlight selected difficulty button
        for i in buttons:
            if button == i:
                i.setStyleSheet("background-color: #9ba2a8")
            else:
                i.setStyleSheet("background-color: #ffffff")

        # change difficulty, and display question
        if button == self.easy_button:
            self.current_difficulty = "Easy"
            self.__display_question(self.current_model, self.current_difficulty)
        elif button == self.intermediate_button:
            self.current_difficulty = "Intermediate"
            self.__display_question(self.current_model, self.current_difficulty)
        elif button == self.difficult_button:
            self.current_difficulty = "Difficult"
            self.__display_question(self.current_model, self.current_difficulty)
        self.current_index = 0  # start at first question

    def __edit_model(self):
        self.current_model = self.comboBox.currentText()
        self.title.setText(f"{self.current_model} Questions")
        self.__display_question(self.current_model, self.current_difficulty)
        self.current_index = 0

    def __insert_preset_questions(self):
        for model, difficulty_levels in self.preset_questions_data.items():
            for difficulty, questions in difficulty_levels.items():
                for question, answer in questions.items():
                    self.__insert_questions(model, difficulty, question, answer)

    @staticmethod
    def __insert_questions(model, difficulty, question, correct_answer):
        insert_question_query = '''
            INSERT INTO Questions(model, difficulty_level, question, correct_answer)
            VALUES (%s, %s, %s, %s)'''

        cursor.execute(insert_question_query, (model, difficulty, question, correct_answer))

        db.commit()

    def __display_question(self, model, difficulty):
        self.answer_text_edit.clear()
        self.result_label.clear()

        question_nodes = self.__get_unanswered_questions(model, difficulty)

        if self.current_index < len(question_nodes):
            if question_nodes[self.current_index].answered_correctly:
                self.current_index += 1
            else:
                self.question_node = question_nodes[self.current_index]
                self.question_label.setText(self.question_node.data)
        else:
            self.question_label.setText("No more questions.")
            self.current_index = 0

    def __submit_question(self):
        answer = self.answer_text_edit.text()
        if answer.lower() == self.question_node.answer:
            self.result_label.setText("Correct!")
            self.question_node.answered_correctly = True
            result = 1
        else:
            self.result_label.setText("Incorrect.")
            result = 0

        query = "SELECT questionID FROM Questions WHERE question = %s"
        cursor.execute(query, (self.question_node.data,))
        record = cursor.fetchone()

        question_id = record[0]

        # check if primary key exists
        check_query = "SELECT COUNT(*) FROM ProgressTracker WHERE questionID = %s AND userID = %s"
        cursor.execute(check_query, (question_id, self.__username))
        record_count = cursor.fetchone()[0]

        if record_count > 0:
            # update the existing record if primary key exists
            update_progress_query = '''
                UPDATE ProgressTracker
                SET answer = %s, result = %s
                WHERE questionID = %s AND userID = %s'''
            cursor.execute(update_progress_query, (answer, result, question_id, self.__username))
        else:
            # insert a new record
            insert_progress_query = '''
                INSERT INTO ProgressTracker(questionID, userID, answer, result)
                VALUES (%s, %s, %s, %s)'''
            cursor.execute(insert_progress_query, (question_id, self.__username, answer, result))

        db.commit()

    def __get_unanswered_questions(self, model, difficulty):
        question_nodes = []
        questions = self.question_tree.get_question(model, difficulty)
        for question in questions:
            if not question.answered_correctly:
                question_nodes.append(question)
        return question_nodes

    def __next_question(self):
        self.answer_text_edit.clear()
        self.result_label.clear()

        question_nodes = self.__get_unanswered_questions(self.current_model, self.current_difficulty)
        if question_nodes:
            # index of the question remains within the bounds
            self.current_index = (self.current_index + 1) % len(question_nodes)
            self.question_node = question_nodes[self.current_index]
            self.question_label.setText(self.question_node.data)
        else:
            self.question_label.setText("All questions have been answered correctly!")
