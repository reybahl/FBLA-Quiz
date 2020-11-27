import mysql.connector

class Connection():
    def create_connection(self):
        self.mydb = mysql.connector.connect(
            host="192.168.1.67",
            user="fbla",
            password="fbla#123"
        )
    
    def close_connection(self):
        self.mydb.close()

    def create_account(self, username, password):
        self.create_connection()
        self.sql = "INSERT INTO FBLA_2021.users(username, password) values (%s, %s)"
        self.val = (username, password)
        self.mycursor = self.mydb.cursor()

        self.mycursor.execute(self.sql, self.val)
        self.mydb.commit()
        self.close_connection()
    
    def login(self, username, password):
        self.create_connection()
        self.sql = "SELECT * from FBLA_2021.users where username = %s and password = %s"
        self.val = (username, password)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(self.sql, self.val)
        self.result = self.mycursor.fetchall()
        
        if len(self.result) == 0:
            return None
        for x in self.result:
            self.ret_val = x
            
        self.close_connection()

        return self.ret_val
        
