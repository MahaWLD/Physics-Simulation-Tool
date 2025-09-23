import pickle


class QuestionNode:     # aggregation
    def __init__(self, data, answer=None, answered_correctly=False):
        self.data = data
        self.answer = answer
        self.answered_correctly = answered_correctly
        self.children = []


class QuestionTree:
    def __init__(self):
        self.root = None

    def build_question_tree(self, question_data):
        self.root = QuestionNode("Questions")
        for model, difficulty_levels in question_data.items():
            model_node = QuestionNode(model)
            for difficulty_level, questions in difficulty_levels.items():
                difficulty_level_node = QuestionNode(difficulty_level)
                for question, answer in questions.items():  # iterate over items to get both question and answer
                    question_node = QuestionNode(question, answer)
                    difficulty_level_node.children.append(question_node)
                model_node.children.append(difficulty_level_node)
            self.root.children.append(model_node)
        return self.root

    def save_tree(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.root, file)

    @staticmethod
    def load_tree(filename):
        with open(filename, 'rb') as file:
            root = pickle.load(file)
        tree = QuestionTree()
        tree.root = root
        return tree

    def traverse_tree(self, node):
        print(node.data, node.answer, node.answered_correctly)
        for child in node.children:
            self.traverse_tree(child)   # recursion

    def get_question(self, model, difficulty_level):
        return self.dfs_find_questions(self.root, model, difficulty_level)

    def dfs_find_questions(self, node, model, difficulty_level):
        if node is None:
            return []   # base case

        if node.data == model and node.children:
            # search for the difficulty level node
            for child in node.children:
                if child.data == difficulty_level:
                    # return all questions under the difficulty level
                    # return [(question_node.data, question_node.answer) for question_node in child.children]
                    return child.children
            return []

        # find questions in under difficulty node
        questions = []
        for child in node.children:
            questions.extend(self.dfs_find_questions(child, model, difficulty_level))     # recursion
        return questions

    def mark_question_answered(self, model, difficulty, question):
        question_nodes = self.dfs_find_questions(self.root, model, difficulty)
        for node in question_nodes:
            if node.data == question:
                node.answered_correctly = True

    def get_model_nodes(self):
        model_nodes = [child for child in self.root.children if child.data != "Questions"]
        return model_nodes

    def add_question(self, model, difficulty_level, question, answer):
        model_node = None
        difficulty_node = None

        # find the model node
        for child in self.root.children:
            if child.data == model:
                model_node = child
                break

        # find the difficulty node
        for child in model_node.children:
            if child.data == difficulty_level:
                difficulty_node = child
                break

        question_node = QuestionNode(question, answer)
        difficulty_node.children.append(question_node)

    def delete_question(self, model, difficulty_level, question):
        model_node = None
        difficulty_node = None

        # find the model node
        for child in self.root.children:
            if child.data == model:
                model_node = child
                break

        # find the difficulty node
        for child in model_node.children:
            if child.data == difficulty_level:
                difficulty_node = child
                break

        for question_node in difficulty_node.children:
            if question_node.data == question:
                difficulty_node.children.remove(question_node)
                break

    def add_model(self, model):
        model_node = QuestionNode(model)
        difficulties = ["Easy", "Intermediate", "Difficult"]
        for level in difficulties:
            difficulty_node = QuestionNode(level)
            model_node.children.append(difficulty_node)

        self.root.children.append(model_node)

    def delete_model(self, model):
        for model_node in self.root.children:
            if model_node.data == model:
                self.root.children.remove(model_node)
                break
