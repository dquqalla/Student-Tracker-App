# Student-Tracker-App
My CRUD application focuses on allowing users, mainly teachers, to be able to track records of their students. 
The files have been commented to give you an idea of how and why I chose to implement certain features the way I did.
For this application I decided to construct my own database using MySQL. 

**For the application I have implemented the following features:**
*  Use of MySQL and SQLAlchemy. 
*  Use of forms and models. 
*  Ability to add new student records.
*  Edit and delete existing student records.
*  Ability for new users to register. 
*  Ability for existing user to delete their account. 
*  Login/logout functionality.
*  Use of flash messages to inform user of success/error. 
*  Examples of success are adding a new record, and examples of error are informing the user if a username currently exists on the database. 
*  Implementation of secure user authentication by using Python werkzeug module. 
*  Werkzeug security hashes password using a salt and hashing method.
*  Use of API which will present all existing student records in a JSON format. This can be accessed by entering the URL... "http://doc.gold.ac.uk/usr/395/api".
*  My own database model.
*  Database called "myapp", consists of two tables "users" and "students".
*  "users" table contains user information, in this case, username and password.
*  "students" table contains student ID, name, email and the ID of the user who created that student record. 

**myapp:**
All the files are located in the myapp folder. The folder consists of several files and subdirectories. 
*  myapp.py - The main application file. Contains all the routes and their respective methods. 
*  forms.py - Used for the login and registration form. Validates user input.
*  dbhelper.py - Uses pymysql to perform MySQL queries on the database "myapp".
*  vs_url_for.py - Used to redirect users successfully.
*  models.py - Uses SQLAlchemy to peform MySQL queries on the database "myapp".

**templates folder:**
Contains the HTML of the website. There are six HTML files.
*  layout.html - The base of the website. Contains the navigation bar. Uses jinja to determine what to present to the user on the navbar.
*  index.html - Main page.
*  login.html - Login page of the site. 
*  register.html - Register page of the site.
*  students.html - Contains the table of the student records. Uses SQLAlchemy methods to retrieve student information and present it to the user. Uses jinja to determine what to present to the user, depending if they are logged in or not.
*  profile.html - Profile page of the user. Displays their username and the ability for the user to delete their account and associated student records tied to it.
