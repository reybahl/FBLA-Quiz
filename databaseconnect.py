import mysql.connector
import random
import firebase_admin
import random
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
            'projectId': 'fir-demo-537d0',
        })
dbref=firestore.client()

class Connection():
    def generate_quiz(self):

        questions_by_type_ref = dbref.collection('questions_by_type')

        self.question_types = ['multiple_choice', 'checkbox', 'fill_in_the_blank', 'true_false']
        self.quiz = []
        random.shuffle(self.question_types)
        for question_type in self.question_types:
            questions_ref = questions_by_type_ref.document(question_type).collection('questions')
            questions_count = len(questions_ref.get())
            question = questions_ref.where('id', '==', random.randrange(0, questions_count - 1)).stream()
            for doc in question:
                self.quiz.append({'type': question_type, 'question' : doc.to_dict()})

        return self.quiz


    def save_results(self, user, results):
        users_ref = dbref.collection('users')
        current_user_quizzes_ref = users_ref.document(user).collection('quiz_results')
        
        current_user_quizzes_ref.add({'results':results})



    def set_prefs(self, user, settings):
        users_ref = dbref.collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')

        current_user_settings_ref.set({'settings': settings})

    def get_prefs(self, user):

        default_settings = {
            'settings': {
            'Name': [''],
            'font': ['12'],
            'Username': [user]
            }
        } 
        users_ref = dbref.collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')
        doc = current_user_settings_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return default_settings   

connection = Connection()
print(connection.get_prefs('myemail@email.com'))     


