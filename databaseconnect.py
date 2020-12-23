import mysql.connector
import random

class Connection():
    def create_connection(self):
        self.mydb = mysql.connector.connect(
            host="192.168.1.67",
            user="fbla",
            password="fbla#123"
        )
    
    def close_connection(self):
        self.mydb.close()

    def execute_sql(self, script, val = ()):
        self.create_connection()
        self.sqlfile = open(script, 'r')
        self.sql = self.sqlfile.read()
        self.val = val
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(self.sql, self.val)

    def create_account(self, username, password):
        self.execute_sql(script= 'register.sql', val=(username, password))
        self.mydb.commit()
        self.close_connection()
    
    def login(self, username, password):
        self.execute_sql(script='login.sql', val=(username, password))
        self.result = self.mycursor.fetchall()
        
        if len(self.result) == 0:
            return None
        for x in self.result:
            self.ret_val = x
            
        self.close_connection()

        return self.ret_val
        
    def generate_quiz(self):
        self.types = ['fillblank', 'mult_choice', 'true_false', 'checkbox'] #These are the different types of questions in a quiz
        random.shuffle(self.types)
        self.questions = []
        for _type in self.types:
            if _type == 'fillblank' or _type == 'true_false':
                self.execute_sql('quizgenerate.sql', (_type,))
                self.question = self.mycursor.fetchall()
                #print(self.question)
                for i, x in enumerate(self.question[0]):
                    if i == 1: 
                        self.name = x
                    if i == 3:
                        self.answer = x
                self.questions.append({'type':_type, 
                                  'name': self.name, 
                                  'answer': self.answer })
            elif _type == 'mult_choice' or _type == 'checkbox':
                self.execute_sql('quizgenerate.sql', (_type,))
                self.question = self.mycursor.fetchall()
                #print(self.question)
                for i, x in enumerate(self.question[0]):
                    if i == 1: 
                        self.name = x
                    if i == 2:
                        if ',' in x:
                            self.options = x.split(',')
                        elif '.' in x:
                            self.options = x.split('.')
                    if i == 3:
                        if ',' in x:
                            self.answer = x.split(',')
                        elif '.' in x:
                            self.answer = x.split('.')
                            
                        else:
                            self.answer = x
                self.questions.append({'type':_type, 
                                  'name': self.name,
                                  'options' : self.options, 
                                  'answer': self.answer}) 
            
        return self.questions

connection = Connection()
connection.generate_quiz()