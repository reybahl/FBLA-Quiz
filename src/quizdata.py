"""FBLA Quiz
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

class QuizData:
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def get_quiz_question_content(self, question_type, doc_dict):
        return {'type': question_type, 'question': doc_dict['content']}
    def check_correct_answer(self):
        pass
    def get_quiz_json(self):
        pass