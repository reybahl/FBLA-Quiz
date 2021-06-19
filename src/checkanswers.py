"""FBLA CheckAnswers
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""
from databaseconnect import Connection
from quizdatafactory import QuizDataFactory

connection = Connection.Instance()


def convert_to_dict(responses):
    """Converts the users responses into a dictionary, 
    the format needed for checking

    :return: A formatted dictionary with the users responses organized by category
    """
    formatted_dict = {}
    matching_dict = {}
    for a, b in responses:
        if b == 'multiple_choice':
            formatted_dict.setdefault(b, []).append(a)
        elif 'matching' in a:
            matching_dict[a.replace('matching_', '')] = b
        else:
            formatted_dict.setdefault(a, []).append(b)
    formatted_dict['matching'] = matching_dict

    return formatted_dict


def check(questions, responses):
    """Checks the user's responses based on the correct question and answer
    """
    responses = convert_to_dict(responses)
    results = []  # Results list

    # Create quiz factory
    quiz_factory = QuizDataFactory()

    for question_object in questions:
        # Factory creates quiz object for the passed in question type
        quiz_object = quiz_factory.create_quiz_object(question_object['type'])
        # Corresponding quiz object for that question type calls the check_correct_answer function.
        results.append(quiz_object.check_correct_answer(question_object, responses))

    score = 0
    for result in results:
        # if the answer is correct
        if result['boolcorrect']:
            # add one to the score
            score += 1

    return results, score
