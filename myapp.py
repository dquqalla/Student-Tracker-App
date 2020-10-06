# Flask Bootstrap
from flask_bootstrap import Bootstrap
# Flask
from flask import Flask, request, render_template, redirect, url_for, session, flash, abort
# Flask Login
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
# FlaskWTF module
from flask_wtf import FlaskForm 
# Custom .py files
from vs_url_for import vs_url_for
# Import models used for SQLAlchemy
from models import db, Users, Students
# Import forms used for validating user input
from forms import loginForm, registerForm
# Import pymsql database and associated functions
from dbhelper import DBHelper
# Password security module
from werkzeug.security import generate_password_hash, check_password_hash
# API import
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
# Configuration of SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myapp_user:myapp_password@localhost/myapp'
app.config['SQLALCHEMY_ECHO'] = False
# Instantiate API
api = Api(app)

# Resource fields, filters output for flask-restful
resource_fields = {
    'id': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'user_id': fields.Integer
}

# Parse and verify the API inputs
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='The ID of the student must be an integer')
parser.add_argument('firstname', type=str, help='The first name of the student must be a string')
parser.add_argument('lastname', type=str, help='The last name of the student must be a string')
parser.add_argument('email', type=str, help='The email of the student must be a string')
parser.add_argument('user_id', type=int, help='The ID of the user must be a integer')

# Instantiating the resource
class StudentsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Students.query.all()

# Assigning a route for the api, to access enter in the URL... "http://doc.gold.ac.uk/usr/395/api"
# Will return all student records in the datbase in a JSON format
api.add_resource(StudentsApi,'/api')

# Initalise Bootstrap for application
Bootstrap(app)
# Initialise pymysql database connection
sqldb = DBHelper()
# Initialise SQLAlchemy database connection
db.init_app(app)
# Initialise flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# Callback function for flask-login
@login_manager.user_loader
def load_user(user_id):
    # User object provided by SQLAlchemy
    return Users.query.get(int(user_id))

# Index route
@app.route('/')
def index():
    # Return index page
    return render_template('index.html')

# Students route
@app.route('/students')
def students():
    # If user is logged in
    if current_user.is_authenticated:
        user_id = current_user.user_id
        # Use SQLAlchemy to retrieve and present student records only created by the user
        students = Students.query.filter_by(user_id = user_id).all()
    else:
        return render_template('students.html')
    
    return render_template('students.html', students=students)

# Inserting new record route
@app.route('/insert', methods = ['GET', 'POST'])
@login_required
def insert():
    if request.method == "POST":
        # Flash message to user
        flash("New student record added successfully.")
        
        # Retrieve form input from user
        student_id = request.form['student_id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        # Use pymsql to add new record using form inputs
        sqldb.addStudent(student_id, firstname, lastname, email, current_user.user_id)

    return redirect(vs_url_for('students'))

# Update students route
@app.route("/update", methods = ['POST', 'GET'])
@login_required
def update():
    if request.method == "POST":
        # Flash message to user informing them of successfull amendment 
        flash("Student record has been amended.")
        
        # Retrieve form input
        id = request.form['id']
        student_id = request.form['student_id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        # Use pymsql to edit student record with form inputs
        sqldb.editStudent(student_id, firstname, lastname, email, id)

    return redirect(vs_url_for('students'))

# Delete students route
@app.route("/delete/<string:student_id>", methods = ['GET'])
@login_required
def delete(student_id):
    if request.method == "GET":
        # Flash message to user 
        flash("Student record deleted.")
        # Call pymsql to delete student record using the student_id associated with the record as an        argument
        sqldb.deleteStudent(student_id)

    return redirect(vs_url_for('students'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Use loginForm() to validate user input
    form = loginForm()
    error = None

    if form.validate_on_submit():
        # Get user object via SQLAlchemy
        user = Users.query.filter_by(username=form.username.data).first()
        # If user exists
        if user:
            # If password matches to user input
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(vs_url_for('index'))
                session['logged_in'] = True
            # Else return flash message informing user password is incorrect
            else:
                flash("Invalid password. Please try again.", "alert alert-danger")
        # If user does not exist, flash message user does not exist
        else:
            error = "User does not exist. Sign up "

    return render_template('login.html', form=form, error=error)

# Logout route
@app.route('/logout')
@login_required
def logout():
    # Logout user 
    logout_user()

    return render_template('index.html', title='Home')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Use registerForm() to validate user input
    form = registerForm()
    # If form is valid
    if form.validate_on_submit():
        # If user already exists
        if Users.query.filter_by(username=form.username.data).first():
            # Flash message
            flash("User already exists.")
        # Otherwise
        else:
            # Hash input password using werkzeug security module
            hashed_pass = generate_password_hash(form.password.data)
            # Assign new variable with username and password input
            user = Users(username=form.username.data, password=hashed_pass)
            # Add user to database
            db.session.add(user)
            # Commit changes
            db.session.commit()
            # Flash message
            flash("Success. Please login.", "alert alert-success")
            # Redirect user to login page
            return redirect(vs_url_for('login'))
   
    return render_template('register.html', form=form)

# Profile route
@app.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    delete = None
    
    # If delete button is clicked...
    if request.method == 'POST':
        # Retrieve user ID of current user
        user_id = current_user.user_id
        # Delete user and associated student records
        db.session.query(Users).filter(Users.user_id == user_id).delete()
        db.session.query(Students).filter(Students.user_id == user_id).delete()
        db.session.commit() 
        # Log user out
        logout_user()
        # Inform user their account has successfully been deleted
        delete = "Your account has been deleted."
        # Return user back to index page
        return render_template('index.html', title='Home', delete=delete)


    return render_template('profile.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
