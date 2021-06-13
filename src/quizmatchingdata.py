"""FBLA Quiz
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from quizdata import QuizData

class QuizMatchingData(QuizData):
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def get_quiz_question_content(self, question_type, doc_dict):
        return {'type': question_type, 'question': doc_dict['question']}

    def check_correct_answer(self, question_object, responses):
        question = question_object['question']
        correct_answer = {k: question['answer'][k] for k in sorted(question['answer'])}
        response = {k: responses['matching'][k] for k in sorted(responses['matching'])}
        shared_items = {k: correct_answer[k] for k in correct_answer if k in response and correct_answer[k] == response[k]}
        boolcorrect = len(shared_items) == len(correct_answer)
        return {'type': question_object['type'],
                        'question': question['content'],
                        'answer': response,
                        'correct': correct_answer,
                        'boolcorrect': boolcorrect}
    def get_quiz_json(self, quiz_json):
        return quiz_json['matching']