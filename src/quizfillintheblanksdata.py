"""FBLA Quiz
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from quizdata import QuizData

class QuizFillInTheBlanksData(QuizData):
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def get_quiz_question_content(self, question_type, doc_dict):
        return {'type': question_type, 'question': doc_dict['content']}

    def check_correct_answer(self, question_object, responses):
            question = question_object['question']
            correct_answer = " or ".join(question['answer']) if type(question['answer']) == list else question['answer']
            lowered_correct_answer = [answer.lower() for answer in question['answer']] 
            return {'type': question_object['type'],
                            'question': question['content'],
                            'answer': responses['fill_in_the_blank'][0],
                             'correct': correct_answer,
                            'boolcorrect': responses[question_object['type']][0].lower() in lowered_correct_answer}
        
    def get_quiz_json(self, quiz_json):
        return quiz_json['fillblank_answer']