class Question:
    def __init__(self, question_id, question, option_a, option_b, option_c, answer, category, value):
        self.question_id = question_id
        self.question = question
        self.option_A = option_a
        self.option_B = option_b
        self.option_C = option_c
        self.answer = answer
        self.category = category
        self.value = value
        self.isAnswered = False
