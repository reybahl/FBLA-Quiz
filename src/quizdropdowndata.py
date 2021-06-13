"""FBLA Quiz
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

from quizdata import QuizData

class QuizDropDownData(QuizData):
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def get_quiz_question_content(self, question_type, doc_dict):
        return {'type': question_type, 'question': doc_dict['content'], 'options': doc_dict['options']}

    def check_correct_answer(self, question_object, responses):
        question = question_object['question']
        correct_answer = question['answer']
        if type(question['answer']) == 'list':
            correct_fixed = [choice.lower() for choice in question['answer']]
            boolcorrect = responses[question_object['type']][0].lower() in correct_fixed
        elif type(question['answer'] == 'str'):
            correct_fixed = question['answer'].lower()
            boolcorrect = responses[question_object['type']][0].lower() == correct_fixed
        return {'type': question_object['type'],
                        'question': question['content'],
                        'answer': responses[question_object['type']][0],
                        'correct': correct_answer,
                        'boolcorrect': boolcorrect}

    def get_quiz_json(self, quiz_json):
        return quiz_json['dropdown_answer']