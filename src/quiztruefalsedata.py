"""FBLA QuizTrueFalseData
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from quizdata import QuizData

class QuizTrueFalseData(QuizData):
    """Specific derived class that contains the functionality for question type: True False. Functinality includes
    getting complete question data from the database, getting actual question, validating responses
    against correct answers.
    """
    def get_quiz_question_content(self, doc_dict):
        """Gets quiz question content for the question type in Json format.
        
        :param doc_dict: Contains the question database document in form of dictionary
        :type doc_dict: dictionary
        :return: Quiz content in Json format.
        """
        return {'type': 'true_false', 'question': doc_dict['content']}

    def check_correct_answer(self, question_object, responses):
        """Checks correct answer and validates user response against the correct answer.
        
        :param question_object: Question Object all the question information (id, question content, correct answer)
        :type question_object: dictionary
        :param responses: Responses selected by the quiz taker (user)
        :type responses: dictionary
        :return: Validated response along with validated answer and boolean indicating whether answer is correct or not
        """
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

    def get_quiz_json(self,  quiz_json):
        """ Gets quiz json corresponding to the current question type object
        
        :param quiz_json: Json containing data for all the question types.
        :return: quiz json corresponding to the current question type object
        """
        return quiz_json['true_false_answer']    