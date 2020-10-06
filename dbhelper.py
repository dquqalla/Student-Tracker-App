# Import pymysql
import pymysql

class DBHelper:
    # Database configuration
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
            user='myapp_user',
            passwd='myapp_password',
            db='myapp',
            autocommit=True)
    
    # Function to add new student record
    def addStudent(self, id, firstname, lastname, email, user_id):
        query = "INSERT INTO students (id, firstname, lastname, email, user_id) VALUES (%s, %s, %s, %s, %s)"
        with self.db.cursor() as cursor:
            # Carry out MySQL query
            cursor.execute(query, (id, firstname, lastname, email, user_id))
            # Commit the change
            return self.db.commit()
    
    # Function to edit existing student record
    def editStudent(self, student_id, firstname, lastname, email, id):
        query = "UPDATE students SET id = %s, firstname = %s, lastname = %s, email = %s WHERE id = %s"
        with self.db.cursor() as cursor:
            # Carry out MySQL query
            cursor.execute(query, (student_id, firstname, lastname, email, id))
            # Commit the change
            return self.db.commit()
    
    # Function to delete existing student record  
    def deleteStudent(self, student_id):
        query = "DELETE FROM students WHERE id = %s"
        with self.db.cursor() as cursor:
            # Carry out MySQL query
            cursor.execute(query, (student_id))
            # Commit the change
            return self.db.commit()

