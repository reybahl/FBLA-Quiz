import mysql.connector

mydb = None

def create_new_connection():
    mydb = mysql.connector.connect(
        host="192.168.1.67",
        user="fbla",
        password="fbla#123"
    )
    print(mydb)
create_new_connection()