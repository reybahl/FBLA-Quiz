import random
import asyncio
from datetime import datetime

from databaseconnect import Connection


class Quiz:
    def generate_quiz(self, user):
        connection = Connection.Instance()
        questions_by_type_ref = connection.getPrimaryDatabase().collection('questions_by_type')
        currentstate_ref = connection.getPrimaryDatabase().collection('users').document(user).collection(
            'quizinprogress').document('currentstate')
        currentstate_ref2 = connection.getBackupDatabase().collection('users').document(user).collection(
            'quizinprogress').document('currentstate')

        self.question_types = ['multiple_choice', 'checkbox', 'fill_in_the_blank', 'true_false', 'matching']
        self.quiz = []
        random.shuffle(self.question_types)
        currentstate_results = []
        for question_type in self.question_types:
            questions_ref = questions_by_type_ref.document(question_type).collection('questions')
            questions_count = len(questions_ref.get())
            if questions_count == 1:
                question = questions_ref.stream()
            else:
                question = questions_ref.where('id', '==', random.randrange(0, questions_count - 1)).stream()
            for doc in question:
                doc_dict = doc.to_dict()
                self.quiz.append({'type': question_type, 'question': doc_dict})
                if question_type == 'multiple_choice' or question_type == 'checkbox':
                    currentstate_question = {'type': question_type, 'question': doc_dict['content'],
                                             'options': doc_dict['options']}
                elif question_type == 'matching':
                    currentstate_question = {'type': question_type, 'question': doc_dict['question']}
                    pass
                else:
                    currentstate_question = {'type': question_type, 'question': doc_dict['content']}
                currentstate_results.append(currentstate_question)
        asyncio.run(
            connection.update_both_databases(db1ref=currentstate_ref, db2ref=currentstate_ref2, ref_type='doc',
                                             task='write',
                                             data={'results': currentstate_results}))
        return self.quiz

    def save_results(self, user, results, score):
        connection = Connection.Instance()
        now = datetime.now()
        now_formatted = now.strftime('%c')
        users_ref = connection.getPrimaryDatabase().collection('users')
        users_ref2 = connection.getBackupDatabase().collection('users')
        current_user_quizzes_ref = users_ref.document(user).collection('quiz_results').document(now_formatted)
        current_user_quizzes_ref2 = users_ref2.document(user).collection('quiz_results').document(now_formatted)

        asyncio.run(connection.update_both_databases(db1ref=current_user_quizzes_ref, db2ref=current_user_quizzes_ref2,
                                                     ref_type='doc', task='write',
                                                     data={'results': results, 'score': score,
                                                           'datetimesubmitted': now_formatted}))

        return now_formatted  # Returns the time it was saved

    def get_quiz_in_progress(self, user):
        connection = Connection.Instance()
        return connection.getPrimaryDatabase().collection('users').document(user).collection('quizinprogress').document(
            'currentstate').get().to_dict()

    def update_quiz_in_progress(self, user, quiz_json):
        connection = Connection.Instance()
        doc_ref1 = connection.getPrimaryDatabase().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')
        doc_ref2 = connection.getBackupDatabase().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')

        questions = doc_ref1.get().to_dict()['results']
        for question in questions:
            if (question['type'] == 'fill_in_the_blank'):
                question['answer'] = quiz_json['fillblank_answer']
            elif (question['type'] == 'true_false'):
                question['answer'] = quiz_json['true_false_answer']
            elif (question['type'] == 'checkbox'):
                question['answer'] = quiz_json['checkbox_answers']
            elif (question['type'] == 'multiple_choice'):
                question['answer'] = quiz_json['multiple_choice_answer']
            elif (question['type'] == 'matching'):
                question['answer'] = quiz_json['matching']
        updatedquiz = {'results': questions}
        asyncio.run(connection.update_both_databases(db1ref=doc_ref1, db2ref=doc_ref2, ref_type='doc', task='write',
                                                     data=updatedquiz))

    def delete_quiz_in_progress(self, user):
        connection = Connection.Instance()
        docref1 = connection.getPrimaryDatabase().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')
        docref2 = connection.getBackupDatabase().collection('users').document(user).collection(
            'quizinprogress').document(
            'currentstate')

        asyncio.run(
            connection.update_both_databases(db1ref=docref1, db2ref=docref2, ref_type='doc', task='del', data=None))

    def get_correct_answers(self, quizqa):
        data = quizqa['results']
        correct_answers = []
        connection = Connection.Instance()
        for entry in data:
            if (entry['type'] == 'matching'):
                docs = connection.getPrimaryDatabase().collection('questions_by_type').document(
                    entry['type']).collection(
                    'questions').where('content', '==', entry['question']['content']).get()
            else:
                docs = connection.getPrimaryDatabase().collection('questions_by_type').document(
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
