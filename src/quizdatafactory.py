"""FBLA QuizDataFactory
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

from quizdropdowndata import QuizDropDownData
from quizfillintheblanksdata import QuizFillInTheBlanksData
from quizmatchingdata import QuizMatchingData
from quizmultiplechoicedata import QuizMultipleChoiceData
from quiztruefalsedata import QuizTrueFalseData


class QuizDataFactory:
    """Factory for creating Quiz object corresponding to the type of question.
    Currently various types of questions are as below ['dropdown', 'multiple_choice', 'fill_in_the_blank',
    'true_false', 'matching'].
    """

    def create_quiz_object(self, question_type):
        """Factory method that creates quiz object for the question type.

        :param question_type: Question type. The values can be one of ['dropdown', 'multiple_choice',
        'fill_in_the_blank', 'true_false', 'matching']
        :type question_type: string
        :return: A Quiz object which contains functionality corresponding to the question type.
        """
        # create and return object corresponding to the question type: Fill in the blanks
        if question_type == 'fill_in_the_blank':
            return QuizFillInTheBlanksData()
        # create and return object corresponding to the question type: Multiple Choice
        elif question_type == 'multiple_choice':
            return QuizMultipleChoiceData()
        # create and return object corresponding to the question type: DropDown
        elif question_type == 'dropdown':
            return QuizDropDownData()
        # create and return object corresponding to the question type: TrueFalse
        elif question_type == 'true_false':
            return QuizTrueFalseData()
        # create and return object corresponding to the question type: Matching
        elif question_type == 'matching':
            return QuizMatchingData()

    def all_quiz_types(self):
        """Returns all quiz types in an array.
        
        :return: Array containing all types of supported question types.
        """
        return ['dropdown', 'multiple_choice', 'fill_in_the_blank', 'true_false', 'matching']
