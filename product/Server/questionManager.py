"""
This module will automatically load the questions from the QS001.json file.
It creates a local list of question objects.

The module can give you a list of available categories or return a question object
given a category (string) or value (integer, which can be 200, 400, 600, 800, or 1000).

Example: 
print(getQuestion("Business",600).answer)
>> B

"""

import json
import random
from os import listdir
from os.path import isfile, join
from product.Common.question import *
from product.Common.questionSet import QuestionSet

PATH_QUESTION_BANK = '../../questionSets'
path_to_json = "../../questionSets/QS001.json"


class QuestionManager:
    def __init__(self):
        self.files = [filename for filename in listdir(PATH_QUESTION_BANK) if
                      isfile(join(PATH_QUESTION_BANK, filename))]

    def get_random_question_set(self):
        # ##### Generate Question Set 1 #####
        selected_filename = self.files[random.randrange(len(self.files)) - 1]
        fp = open(join(PATH_QUESTION_BANK, selected_filename))
        raw_data = json.load(fp)
        # Open the json file and use it to create a list of question objects called question_set
        question_set = QuestionSet()
        question_set.id = selected_filename
        for d in raw_data:
            question = Question(d["question_id"], d["question"], d["option_A"], d["option_B"],
                                d["option_C"], d["answer"], d["category"], d["value"])
            question_set.add_question(question)
            if d['question_id'] % 5 == 1:
                question_set.categories[int(d['question_id'] / 5)] = d['category']
        print(question_set.categories)
        fp.close()
        # ##### Generate Question Set 2 #####
        selected_filename2 = self.files[random.randrange(len(self.files)) - 1]
        while selected_filename == selected_filename2:
            selected_filename2 = self.files[random.randrange(len(self.files)) - 1]
        # print(f'Selected {selected_filename}')
        # print(f'Selected {selected_filename2}')
        fp = open(join(PATH_QUESTION_BANK, selected_filename2))
        raw_data = json.load(fp)
        # Open the json file and use it to create a list of question objects called question_set
        question_set2 = QuestionSet()
        question_set2.id = selected_filename2
        for d in raw_data:
            question = Question(d["question_id"], d["question"], d["option_A"], d["option_B"],
                                d["option_C"], d["answer"], d["category"], d["value"])
            question_set2.add_question(question)
            if d['question_id'] % 5 == 1:
                question_set2.categories[int(d['question_id'] / 5)] = d['category']
        print(question_set2.categories)
        fp.close()
        return question_set, question_set2


# Test code
if __name__ == '__main__':
    qm = QuestionManager()
    qs, qs2 = qm.get_random_question_set()
    cat = qs.get_list_of_categories()
    print(f'{len(cat)} categories: {cat}')
    a_question = qs.get_question(cat[1])
    print(f'{a_question}')
    print(f'{a_question.question}')
