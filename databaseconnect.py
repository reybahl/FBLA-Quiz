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
    # def __init__(self):
    #     self.connect()

    # def create_connection(self):
    #     self.mydb = mysql.connector.connect(
    #         host="192.168.1.67",
    #         user="fbla",
    #         password="fbla#123"
    #     )

    # def close_connection(self):
    #     self.mydb.close()

    # def execute_sql(self, script, val = ()):
    #     self.create_connection()
    #     self.sqlfile = open(script, 'r')
    #     self.sql = self.sqlfile.read()
    #     self.val = val
    #     self.mycursor = self.mydb.cursor()
    #     self.mycursor.execute(self.sql, self.val)

    # def create_account(self, username, password):
    #     self.execute_sql(script= 'register.sql', val=(username, password))
    #     self.mydb.commit()
    #     self.close_connection()

    # def login(self, username, password):
    #     self.execute_sql(script='login.sql', val=(username, password))
    #     self.result = self.mycursor.fetchall()

    #     if len(self.result) == 0:
    #         return None
    #     for x in self.result:
    #         self.ret_val = x

    #     self.close_connection()

    #     return self.ret_val

    # def connect(self):
    #     pass

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

    def store_prefs(self, user, settings):
        users_ref = dbref.collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')

        current_user_settings_ref.set({'settings': settings})



connection = Connection()
print(connection.generate_quiz())