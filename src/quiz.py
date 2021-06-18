"""FBLA Quiz
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

import random
import asyncio
from datetime import datetime
from pytz import timezone

from databaseconnect import Connection
from quizdatafactory import QuizDataFactory


class Quiz:
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """

    def generate_quiz(self, user):
        """Generates a new quiz. There are 5 types of questions and in all more than 50 questions 
        that are stored in firestore database, which is a NoSQL document oriented 
        database. Questions are stored in the database in a tree form with a question
        type being a parent node. Each question in each question type contains an id.
        This function uses python class :class:`random.Random` to generate a random id
        and then uses that id to fetch a question.

        :param user: user email for which we want to generate a new quiz. The quiz then gets associated
                    with that user
        :type user: string
        :return: A complete Quiz object which contains 5 different types of randomly generated questions
        """
        # Get Singleton connection instance
        connection = Connection.Instance()
        questions_by_type_ref = connection.get_primary_database().collection('questions_by_type')
        currentstate_ref = connection.get_primary_database().collection('users').document(user).collection(
            'quizinprogress').document('currentstate')
        currentstate_ref_backup = connection.get_backup_database().collection('users').document(user).collection(
            'quizinprogress').document('currentstate')

        # Create quiz data factory
        quiz_factory = QuizDataFactory()
        self.question_types = quiz_factory.all_quiz_types()

        quiz = []
        random.shuffle(self.question_types)
        currentstate = []
        for question_type in self.question_types:
            questions_ref = questions_by_type_ref.document(question_type).collection('questions')
            questions_count = len(questions_ref.get())
            if questions_count == 1:
                question = questions_ref.stream()
            else:
                question = questions_ref.where('id', '==', random.randrange(0,
                                                                            questions_count - 1)).stream()  # Gets random question from category based upon amount of questions in that category
            for doc in question:
                doc_dict = doc.to_dict()
                quiz.append({'type': question_type, 'question': doc_dict})
                quiz_object = quiz_factory.create_quiz_object(question_type)
                currentstate_question = quiz_object.get_quiz_question_content(doc_dict)
                currentstate.append(currentstate_question)
        eastern = timezone('US/Eastern')
        quiz_start_time = datetime.now(eastern)
        asyncio.run(connection.update_both_databases(primary_db=currentstate_ref, backup_db=currentstate_ref_backup,
                                                     ref_type='doc',
                                                     task='write',
                                                     data={'results': currentstate, 'startTime': quiz_start_time}))
        return quiz

    def save_results(self, user, results, score, time_taken):
        """Saves quiz results in the database for a particular user. The results contains the actual
        answers that user selected as well the correct answers for future report generation and comparison
        
        This function also support dynamic backup feature where it writes asynchronously to a primary database and
        secondary (backup) database. It internally uses :class:`asyncio` to asynchronously update both databases.

        :param user: user email for which we want to generate a new quiz. The quiz then gets associated
                    with that user
        :type user: string
        :param results: actual results that contain the answers given by the user and correct answers
        :type results: dictionary
        :param score: score for the quiz taken by the user
        :type score: integer
        :param time_taken: time taken by the user to complete the quiz (in the format: mm:ss)
        :type time_taken: string
        :return: A complete Quiz object which contains 5 different types of randomly generated questions
        """
        connection = Connection.Instance()
        eastern = timezone('US/Eastern')
        current_time = datetime.now(eastern)
        now_formatted = current_time.strftime('%b %d %Y %I:%M%p')
        users_primary_db = connection.get_primary_database().collection('users')
        users_backup_db = connection.get_backup_database().collection('users')
        current_user_quizzes_primary_ref = users_primary_db.document(user).collection('quiz_results').document(
            now_formatted)
        current_user_quizzes_backup_ref = users_backup_db.document(user).collection('quiz_results').document(
            now_formatted)

        asyncio.run(connection.update_both_databases(primary_db=current_user_quizzes_primary_ref,
                                                     backup_db=current_user_quizzes_backup_ref,
                                                     ref_type='doc', task='write',
                                                     data={'results': results, 'score': score,
                                                           'datetimesubmitted': now_formatted,
                                                           'timetaken': time_taken}))

        return now_formatted  # Returns the time it was saved

    def get_quiz_in_progress(self, user):
        """Gets a quiz in progress for the user email passed in as a param from the primary database
        instance.

        :param user: user email for which we want to get quiz in progress.
        :type user: string
        :return: A complete current Quiz in progress object
        """
        connection = Connection.Instance()
        return connection.get_primary_database().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate').get().to_dict()

    def update_quiz_in_progress(self, user, quiz_json):
        """Updates quiz in progress for the user email passed in as a param to both primary
        and backup database instances.
        
        :param user: user email for which we want to get quiz in progress.
        :type user: string
        
        :param quiz_json: contains the quiz object populated from the UI based upon 
                          user selection
        :type quiz_json: JSON string
        """
        connection = Connection.Instance()
        quiz_in_progress_primary_ref = connection.get_primary_database().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')
        quiz_in_progress_backup_ref = connection.get_backup_database().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')

        questions = quiz_in_progress_primary_ref.get().to_dict()['results']
        start_time = quiz_in_progress_primary_ref.get().to_dict()['startTime']
        quiz_factory = QuizDataFactory()
        for question in questions:
            quiz_object = quiz_factory.create_quiz_object(question['type'])
            question['answer'] = quiz_object.get_quiz_json(quiz_json)
        updated_quiz = {'results': questions, 'timeTaken': quiz_json['timeTaken'],
                        'startTime': start_time}
        asyncio.run(connection.update_both_databases(primary_db=quiz_in_progress_primary_ref,
                                                     backup_db=quiz_in_progress_backup_ref, ref_type='doc', task='write',
                                                     data=updated_quiz))

    def delete_quiz_in_progress(self, user):
        """Deletes quiz in progress for the user email passed in as a param from both primary
        and backup database instances. This function gets called when user has submitted a quiz
        and completed. At that point there would be no quiz in progress associated with a user.
        
        :param user: user email for which we want to get quiz in progress.
        :type user: string
        """
        connection = Connection.Instance()
        quiz_in_progress_primary_ref = connection.get_primary_database().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')
        quiz_in_progress_backup_ref = connection.get_backup_database().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')

        asyncio.run(connection.update_both_databases(primary_db=quiz_in_progress_primary_ref,
                                                     backup_db=quiz_in_progress_backup_ref, ref_type='doc', task='del',
                                                     data=None))

    def get_correct_answers(self, quizqa):
        """Matches answers submitted by the user with the correct answers stored in the database.
        
        :param quizqa: contains answers submitted by the user.
        :type quizqa: dictionary
        :return: Questions that were answered correctly by the user.
        """
        data = quizqa['results']
        correct_answers = []
        connection = Connection.Instance()
        for entry in data:
            if entry['type'] == 'matching':
                docs = connection.get_primary_database().collection('questions_by_type').document(
                    entry['type']).collection(
                    'questions').where('content', '==', entry['question']['content']).get()
            else:
                docs = connection.get_primary_database().collection('questions_by_type').document(
                    entry['type']).collection(
                    'questions').where('content', '==', entry['question']).get()
            for doc in docs:
                returned_doc = doc.to_dict()
                question = {}
                correct_answers_entry = {}
                question['content'] = entry['question'] if entry['type'] != 'matching' else entry['question']['content']
                question['answer'] = returned_doc['answer']
                correct_answers_entry['question'] = question
                correct_answers_entry['type'] = entry['type']
                correct_answers.append(correct_answers_entry)

        return correct_answers
