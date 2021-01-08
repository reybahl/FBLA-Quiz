import random
import firebase_admin
import random
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import asyncio

cred = credentials.Certificate("serviceAccountKey.json")
app1= firebase_admin.initialize_app(cred, {
            'projectId': 'fir-demo-537d0',
        }, name='app1')
dbref=firestore.client(app1)

cred2 = credentials.Certificate("serviceAccountKey2.json")
app2= firebase_admin.initialize_app(cred2, {
            'projectId': 'firestoredemo-2',
        }, name='app2')
dbref2=firestore.client(app2)

class Connection():
    async def update_dbref_1(self, ref, ref_type, task, data = None):
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_dbref_2(self, ref, ref_type, task, data = None):
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_both_databases(self, db1ref, db2ref, ref_type, task, data):
        #Updates both databases
        await asyncio.gather(self.update_dbref_1(db1ref, ref_type, task, data), self.update_dbref_2(db2ref, ref_type, task, data))
        

    def generate_quiz(self, user):

        questions_by_type_ref = dbref.collection('questions_by_type')
        currentstate_ref = dbref.collection('users').document(user).collection('quizinprogress').document('currentstate')
        currentstate_ref2 = dbref2.collection('users').document(user).collection('quizinprogress').document('currentstate')

        self.question_types = ['multiple_choice', 'checkbox', 'fill_in_the_blank', 'true_false', 'matching']
        self.quiz = []
        random.shuffle(self.question_types)
        currentstate_results = []
        for question_type in self.question_types:
            questions_ref = questions_by_type_ref.document(question_type).collection('questions')            
            questions_count = len(questions_ref.get())
            if(questions_count == 1):
                question = questions_ref.stream()
            else:
                question = questions_ref.where('id', '==', random.randrange(0, questions_count - 1)).stream()
            for doc in question:
                doc_dict = doc.to_dict()
                self.quiz.append({'type': question_type, 'question' : doc_dict})
                if(question_type == 'multiple_choice' or question_type == 'checkbox'):
                    currentstate_question = {'type': question_type, 'question': doc_dict['content'], 'options': doc_dict['options']}
                elif(question_type == 'matching'):
                    currentstate_question = {'type': question_type, 'question': doc_dict['question']}
                    pass
                else:
                    currentstate_question = {'type': question_type, 'question': doc_dict['content']}
                currentstate_results.append(currentstate_question)
        asyncio.run(self.update_both_databases(db1ref = currentstate_ref, db2ref = currentstate_ref2, ref_type = 'doc', task = 'write', data = {'results': currentstate_results}))
        return self.quiz


    def save_results(self, user, results, score):

        now = datetime.now()
        now_formatted = now.strftime('%c')
        users_ref = dbref.collection('users')
        users_ref2 = dbref2.collection('users')
        current_user_quizzes_ref = users_ref.document(user).collection('quiz_results').document(now_formatted)
        current_user_quizzes_ref2 = users_ref2.document(user).collection('quiz_results').document(now_formatted)
        
        asyncio.run(self.update_both_databases(db1ref= current_user_quizzes_ref, db2ref =current_user_quizzes_ref2, ref_type='doc', task='write', data={'results' : results, 'score' : score, 'datetimesubmitted' : now_formatted}))

        return now_formatted #Returns the time it was saved



    def set_prefs(self, user, settings):
        users_ref = dbref.collection('users')
        users_ref2 = dbref2.collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')
        current_user_settings_ref2 = users_ref2.document(user).collection('settings').document('settings')

        asyncio.run(self.update_both_databases(db1ref= current_user_settings_ref, db2ref =current_user_settings_ref2, ref_type='doc', task='write', data={'settings': settings}))

    def get_prefs(self, user):

        default_settings = {
            'settings': {
            'Name': [''],
            'font': ['12'],
            'Username': [user],
            'checkbox' : ['showwronganswer']
            }
        } 
        users_ref = dbref.collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')
        doc = current_user_settings_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return default_settings 

    def get_reports(self, user):

        users_ref = dbref.collection('users')
        docs = users_ref.document(user).collection('quiz_results').stream()
        reports = []
        for doc in docs:
            reports.append({
                'datetime' : doc.id,
                'score' : doc.to_dict()['score']
            })

        return reports
        #print(reports)

    def get_report_for_date(self, user, datetime):
        users_ref = dbref.collection('users')
        doc = users_ref.document(user).collection('quiz_results').document(datetime).get()
        return doc.to_dict()

    def get_quiz_in_progress(self, user):
        return dbref.collection('users').document(user).collection('quizinprogress').document(
            'currentstate').get().to_dict()
    def update_quiz_in_progress(self, user, quiz_json):
        doc_ref1 = dbref.collection('users').document(user).collection('quizinprogress').document(
            'currentstate')
        doc_ref2 = dbref2.collection('users').document(user).collection('quizinprogress').document(
        'currentstate')

        questions = doc_ref1.get().to_dict()['results']
        for question in questions:
            if(question['type'] == 'fill_in_the_blank'):
                question['answer'] = quiz_json['fillblank_answer']
            elif(question['type'] == 'true_false'):
                question['answer'] = quiz_json['true_false_answer']
            elif (question['type'] == 'checkbox'):
                question['answer'] = quiz_json['checkbox_answers']
            elif (question['type'] == 'multiple_choice'):
                question['answer'] = quiz_json['multiple_choice_answer']
            elif (question['type'] == 'matching'):
                question['answer'] = quiz_json['matching']
        updatedquiz = {'results': questions}
        asyncio.run(self.update_both_databases(db1ref=doc_ref1, db2ref=doc_ref2, ref_type='doc', task='write', data= updatedquiz))
    
    def delete_quiz_in_progress(self, user):
        docref1 = dbref.collection('users').document(user).collection('quizinprogress').document('currentstate')
        docref2 = dbref2.collection('users').document(user).collection('quizinprogress').document('currentstate')

        asyncio.run(self.update_both_databases(db1ref = docref1, db2ref= docref2, ref_type='doc', task='del', data=None))

    def get_help(self, question_json):
        classification = self.classify(question_json['question'])
        qas = dbref.collection('help').document(classification).collection('Q&A').stream()
        qaarr = []
        for doc in qas:
            qa = doc.to_dict()
            qaarr.append(qa)
        return qaarr
    def classify(self, question):
        data = dbref.collection('intelligent_help')
        docs = data.stream()
        training_data = []
        for doc in docs:
            training_data.append((doc.to_dict()['text'], doc.to_dict()['label']))
        cl = NaiveBayesClassifier(training_data)
        text_tokens = word_tokenize(question)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        filtered_question = (" ").join(tokens_without_sw)
        return cl.classify(filtered_question)
    def get_correct_answers(self, quizqa):
        data = quizqa['results']
        correct_answers = []
        for entry in data:
            if (entry['type'] == 'matching'):
                docs = dbref.collection('questions_by_type').document(entry['type']).collection('questions').where('content', '==', entry['question']['content']).get()
            else:
                docs = dbref.collection('questions_by_type').document(entry['type']).collection('questions').where('content', '==', entry['question']).get()
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
    def get_frequently_asked_questions(self):
        questions = []
        qa = dbref.collection('help')
        docs = qa.stream()
        for doc in docs:
            category = doc.id
            questions_of_category = qa.document(category).collection('Q&A').stream()
            for question in questions_of_category:
                questions.append({'question' : question.to_dict()['question'],
                                  'answer' : question.to_dict()['answer']})
        return questions


connection = Connection()
print("done")