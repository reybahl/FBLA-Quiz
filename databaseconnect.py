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
        self.execute_sql(script= 'sqlscripts/register.sql', val=(username, password))
        self.mydb.commit()
        self.close_connection()
    
    def login(self, username, password):
        self.execute_sql(script='sqlscripts/login.sql', val=(username, password))
        self.result = self.mycursor.fetchall()
        
        if len(self.result) == 0:
            return None
        for x in self.result:
            self.ret_val = x
            
        self.close_connection()

        return self.ret_val
    def generate_quiz():
        types = ['fillblank', 'mult_choice', 'true_false', 'checkbox'] #These are the different types of questions in a quiz
        random.shuffle(types)
        questions = []
        for _type in types:
            if _type == 'fillblank' or _type == 'true_false':
                questions.append({'type':_type})
            elif _type == 'mult_choice' or _type == 'checkbox':
                questions.append({'type' : _type, choices : []}) 
            
        return questions
