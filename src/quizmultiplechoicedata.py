"""FBLA Quiz
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from quizdata import QuizData

class QuizMultipleChoiceData(QuizData):
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def get_quiz_question_content(self, question_type, doc_dict):
        return {'type': question_type, 'question': doc_dict['content'],
                'options': doc_dict['options'], 'correct_answer': doc_dict['answer']}

    def check_correct_answer(self, question_object, responses):
        question = question_object['question']
        correct_answer = question['answer'] if type(question['answer']) == str else ", ".join(question['answer'])
        #Sorts answer if it is a list
        correct_sorted = sorted(question['answer']) if type(question['answer']) == list else question['answer']
        #lowers all the answer choices
        correct_lowered = correct_sorted.lower() if type(correct_sorted) == str else [x.lower() for x in correct_sorted]
        response = ", ".join(responses['multiple_choice']) if type(responses['multiple_choice']) == list else responses['multiple_choice']
        response_sorted = sorted(responses['multiple_choice']) if len(responses['multiple_choice']) > 1 else responses['multiple_choice'][0]
        response_lowered = response_sorted.lower() if type(response_sorted) == str else [x.lower() for x in response_sorted]
        return {'type': question_object['type'],
                        'question': question['content'],
                        'answer': response,
                        'correct': correct_answer,
                        'boolcorrect': response_lowered == correct_lowered}

    def get_quiz_json(self, quiz_json):
        return quiz_json['multiple_choice_answers']