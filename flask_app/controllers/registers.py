from flask_app.__init__ import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe
from flask_app.models.register import Register
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def home_page():
    if 'account_id' not in session:
        flash('Must be logged in!!!!', 'bad')
        return redirect('/')
    data = {
        'id': session['account_id']
    }
    recipes = Recipe.get_all_recipes()
    user = Register.get_by_id(data)
    return render_template('dashboard.html', user=user, recipes = recipes)

@app.route('/register', methods=['POST'])
def create_account():
    if not Register.validate_account(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    account_id = Register.save(data)
    session['account_id'] = account_id
    
    return redirect('/dashboard')

@app.route('/login', methods=['POST']) 
def login():
    data = {"email": request.form['email']}
    account = Register.get_by_email(data)
    if not account:
        flash("Invalid Email/Password", 'bad')
        return redirect('/')
    if not bcrypt.check_password_hash(account.password, request.form['password']):
        flash("Invalid Email/Password",'bad')
        return redirect('/')

    session['account_id'] = account.id

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

