"""FBLA QuizMultipleChoiceData
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from quizdata import QuizData

class QuizMultipleChoiceData(QuizData):
    """Specific derived class that contains the functionality for question type: Multiple Choice. Functinality includes
    getting complete question data from the database, getting actual question, validating responses
    against correct answers.
    """
    def get_quiz_question_content(self, doc_dict):
        """Gets quiz question content for the question type in Json format.
        
        :param doc_dict: Contains the question database document in form of dictionary
        :type doc_dict: dictionary
        :return: Quiz content in Json format.
        """
        return {'type': 'multiple_choice', 'question': doc_dict['content'],
                'options': doc_dict['options'], 'correct_answer': doc_dict['answer']}

    def check_correct_answer(self, question_object, responses):
        """Checks correct answer and validates user response against the correct answer.
        
        :param question_object: Question Object all the question information (id, question content, correct answer)
        :type question_object: dictionary
        :param responses: Responses selected by the quiz taker (user)
        :type responses: dictionary
        :return: Validated response along with validated answer and boolean indicating whether answer is correct or not
        """
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
        """ Gets quiz json corresponding to the current question type object
        
        :param quiz_json: Json containing data for all the question types.
        :return: quiz json corresponding to the current question type object
        """
        return quiz_json['multiple_choice_answers']