from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])[a-zA-Z\d]{8,45}$') # THANKS TA KOS
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,45}$')

class Register:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod 
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s); "
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        if result == False  or len(result) < 1  :
            return False
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        if result == False  or len(result) < 1  :
            return False
        return cls(result[0])

    @staticmethod
    def validate_account(account):
        is_valid = True
        if not NAME_REGEX.match(account['first_name']):
            flash("First Name must be atleast 2 characters and only letters", 'error')
            is_valid = False
        if not NAME_REGEX.match(account['last_name']):
            flash("Last Name must be atleast 2 characters and only letters", 'error')
            is_valid = False
        if not EMAIL_REGEX.match(account['email']):
            flash('Invalid email address!', 'error')
            is_valid = False
        if Register.get_by_email(account) != False : #thanks TA Kos if its is false it found the email if not theres no email
            flash('Email already in use', 'error')
            is_valid = False
        if not PASSWORD_REGEX.match(account['password']):
            flash('Password cannot be empty and needs atleast one uppercase letter, one lowercase letter, and one number(MIN of 8 characters ) ', 'error')
            is_valid = False
        if account['password'] != account['confirm_password']:
            flash("Passwords do not match!", 'error')
            is_valid = False
        return is_valid

