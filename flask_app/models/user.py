# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# model the class after the friend table from our database

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO validation ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('registration').query_db( query, data )

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM validation WHERE email = %(email)s;"
        result = connectToMySQL("registration").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False    
        return cls(result[0])

    @classmethod
    def get_username(cls,num):
        query = "SELECT * FROM validation WHERE id = {};".format(num)
        return connectToMySQL("registration").query_db(query)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        return is_valid
