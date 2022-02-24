from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
from flask_app.models.register import Register
import re
from datetime import date

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instructions']
        self.made_on = data['made_on']
        self.mins_orless = data['30mins_orless']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
        self.owner = []

    @staticmethod
    def validate_recipe(data):
        is_valid=True
        if '30min_orless' not in data:
            is_valid = False
            flash('30 minutes or less must be filled out')
        if len(data['name']) < 3:
            is_valid = False
            flash("Recipe name must be more than 3 characters long")
        if len(data['description']) < 3:
            is_valid = False
            flash("Recipe description must be more than 3 characters long")
        if len(data['instr']) < 3:
            is_valid = False
            flash("Recipe instructions must be more than 3 characters long")
        now = date.today()
        made_date = data['made_on']
        then = date(year = int(made_date[0:4]), month = int(made_date[5:7]), 
        day = int(made_date[8:10]))
        if then > now:
            is_valid = False
            flash("Can't be a future date")
        return is_valid

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for row in results:
            user_data = {
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            sin_recipe = cls(row)
            sin_recipe.owner = Register(user_data)
            recipes.append(sin_recipe)
        return recipes
        
    @classmethod
    def add_recipes(cls,data):
        query = "INSERT INTO recipes(name,description,instructions,made_on,30mins_orless, user_id) VALUES(%(name)s,%(description)s,%(instr)s,%(made_on)s,%(30min_orless)s, %(user_id)s);"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def show_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        if result == False  or len(result) < 1  :
            return False
        return cls(result[0])

    @classmethod 
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions =  %(instr)s ,made_on = %(made_on)s, 30mins_orless =%(30min_orless)s WHERE id = %(recipe_id)s;"  
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query,data)