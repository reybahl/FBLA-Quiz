"""FBLA Quiz
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from quizdropdowndata import QuizDropDownData
from quizfillintheblanksdata import QuizFillInTheBlanksData
from quizmatchingdata import QuizMatchingData
from quizmultiplechoicedata import QuizMultipleChoiceData
from quiztruefalsedata import QuizTrueFalseData

class QuizDataFactory:
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def create_quiz_object(self, typ):
        if(typ == 'fill_in_the_blank'):
            return QuizFillInTheBlanksData()
        elif(typ == 'multiple_choice'):
            return QuizMultipleChoiceData()
        elif(typ == 'dropdown'):
            return QuizDropDownData()
        elif(typ == 'true_false'):
            return QuizTrueFalseData()
        elif(typ == 'matching'):
            return QuizMatchingData()

    def all_quiz_types(self):
        return ['dropdown', 'multiple_choice', 'fill_in_the_blank', 'true_false', 'matching']
