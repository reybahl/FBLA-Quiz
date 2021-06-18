"""FBLA QuizMatchingData
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from quizdata import QuizData


class QuizMatchingData(QuizData):
    """Specific derived class that contains the functionality for question type: Matching. Functinality includes
    getting complete question data from the database, getting actual question, validating responses
    against correct answers.
    """

    def get_quiz_question_content(self, doc_dict):
        """Gets quiz question content for the question type in Json format.
        
        :param doc_dict: Contains the question database document in form of dictionary
        :type doc_dict: dictionary
        :return: Quiz content in Json format.
        """
        return {'type': 'matching', 'question': doc_dict['question']}

    def check_correct_answer(self, question_object, responses):
        """Checks correct answer and validates user response against the correct answer.
        
        :param question_object: Question Object all the question information (id, question content, correct answer)
        :type question_object: dictionary
        :param responses: Responses selected by the quiz taker (user)
        :type responses: dictionary
        :return: Validated response along with validated answer and boolean indicating whether answer is correct or not
        """
        question = question_object['question']
        correct_answer = {k: question['answer'][k] for k in sorted(question['answer'])}
        response = {k: responses['matching'][k] for k in sorted(responses['matching'])}
        shared_items = {k: correct_answer[k] for k in correct_answer if
                        k in response and correct_answer[k] == response[k]}
        boolcorrect = len(shared_items) == len(correct_answer)
        return {'type': question_object['type'],
                'question': question['content'],
                'answer': response,
                'correct': correct_answer,
                'boolcorrect': boolcorrect}

    def get_quiz_json(self, quiz_json):
        """ Gets quiz json corresponding to the current question type object
        
        :param quiz_json: Json containing data for all the question types.
        :return: quiz json corresponding to the current question type object
        """
        return quiz_json['matching']
