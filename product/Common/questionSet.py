class QuestionSet:
    def __init__(self):
        self.id = ...
        self.questions = []
        self.categories = {}

    def add_question(self, question):
        self.questions.append(question)

    # Returns a question given a category and a value
    def get_question(self, category):
        for q in self.questions:
            if q.category == category and q.isAnswered is False:
                return q
        return None

    def get_categories(self):
        return self.categories

    # Returns a list of all categories presented in the question set
    def get_list_of_categories(self):
        categories = []
        for q in self.questions:
            if q.category not in categories:
                categories.append(q.category)
        return categories

    def has_unanswered_question(self):
        for q in self.questions:
            if q.isAnswered is False:
                return True
        return False

    def get_categories_status(self):
        is_answered = [False] * 31
        category_done = [True] * 6
        for q in self.questions:
            is_answered[q.question_id] = q.isAnswered
        for i in range(1, 6):
            if is_answered[i] is False:
                category_done[0] = False
        # for i in range(6, 7):
        for i in range(6, 11):
            if is_answered[i] is False:
                category_done[1] = False
        # for i in range(11, 12):
        for i in range(11, 16):
            if is_answered[i] is False:
                category_done[2] = False
        # for i in range(16, 17):
        for i in range(16, 21):
            if is_answered[i] is False:
                category_done[3] = False
        for i in range(21, 26):
            if is_answered[i] is False:
                category_done[4] = False
        for i in range(26, 31):
            if is_answered[i] is False:
                category_done[5] = False
        return category_done
