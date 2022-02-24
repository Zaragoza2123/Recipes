from flask_app.__init__ import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe
from flask_app.models.register import Register

@app.route('/sendtocreate_recipe' )
def send_to_form():
    return render_template('create_recipe.html')

@app.route('/create_recipe', methods=['POST'])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/sendtocreate_recipe')
    Recipe.add_recipes(request.form)
    return redirect('/dashboard')

@app.route('/view_instructions/<int:recipe_id>')
def show_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    data1 = {
        'id': session['account_id']
    }
    user = Register.get_by_id(data1)
    recipes = Recipe.show_recipe_by_id(data)
    return render_template('instructions.html' , user = user, recipes = recipes)

@app.route('/update_recipe/<int:recipe_id>')
def editpage(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.show_recipe_by_id(data)
    recipe.made_on = str(recipe.made_on)[0:10]
    return render_template('recipe_edit.html', recipe = recipe)

@app.route('/edit_recipe/<int:recipe_id>',methods=['POST'])
def update_recipe(recipe_id):
    data = {
        "recipe_id": recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instr': request.form['instr'],
        'made_on': request.form['made_on'],
        '30min_orless': request.form['30min_orless']
    }
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/update_recipe/{recipe_id}')
    else:
        Recipe.update_recipe(data)
        return redirect('/dashboard')

@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')