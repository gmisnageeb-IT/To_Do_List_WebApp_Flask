from flask import Flask ,render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
Scss(app) #initialize the SCSS extension to enable SCSS support in the Flask application. it allows you to write stylesheets using SCSS syntax and have them automatically compiled into CSS when the application runs.

# configure the SQLite database, relative to the app instance folder
#configure the database URI for SQLAlchemy to use SQLite as the database engine and specify the location of the database file (database.db) relative to the app instance folder. This allows the application to connect to and interact with the SQLite database.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" 

#For deployment in web only(you can remove it if you run it in local machine): no need to save the track of add/delete/update logs to make it fast
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #disable the SQLAlchemy event system that tracks modifications to objects and emits signals. This is done to save memory and improve performance, as the application does not require this feature.

##Flask connect with db: initialize the SQLAlchemy extension to enable database functionality in the Flask application. It allows you to interact with a database using Python objects and provides an ORM (Object-Relational Mapping) layer for easier database management.
db = SQLAlchemy(app) 

#create a class to represent the task table in the database. The class will inherit from db.Model, which is a base class provided by SQLAlchemy for defining database models. Each instance of the MyTask class will represent a row in the task table, and each attribute of the class will represent a column in the table.
#each row in the table will be represented as an instance of the MyTask class, and each column in the table will be represented as an attribute of the User class. The db.Model base class provides methods for querying, inserting, updating, and deleting records in the database.
#pass objects to the database and retrieve data from it using Python code instead of writing raw SQL queries.
#to create the database table by the Class MyTask. we will define the columns of the table as attributes of the MyTask class. Each attribute will be defined using the db.Column class, which specifies the data type and constraints for the column. 
#we will fill the table with data using the MyTask class and retrieve data from it using SQLAlchemy queries.
class MyTask(db.Model): #create a class called MyTask that inherits from db.Model, which is the base class for all models in SQLAlchemy. This class will represent the task table in the database.
    id = db.Column(db.Integer, primary_key=True) #define the columns of the table. The id column is an integer and serves as the primary key for the table.
    content = db.Column(db.String(100), nullable=False) #The name column is a string with a maximum length of 80 characters and cannot be null (nullable=False).
    completed = db.Column(db.Integer, default = 0) #The email column is a string with a maximum length of 120 characters, must be unique (unique=True), and cannot be null.
    created = db.Column(db.DateTime, default = datetime.utcnow) #The created_at column is a DateTime field that will automatically be set to the current timestamp when a new record is created.

    #on html page, when we print the object of MyTask class, it will call the __repr__ method to get a string representation of the object. This is useful for debugging and logging purposes, as it allows you to easily identify instances of the MyTask class when printed or logged.
    def __repr__(self)-> str: 
        return f"Task {self.id}" #return a string representation of the MyTask object, which includes the task's id. This is useful for debugging and logging purposes, as it allows you to easily identify instances of the MyTask class when printed or logged.

#create the database table
#to ensure that the database operations are performed within the context of the Flask application. This is necessary because certain operations, such as creating tables, require access to the application context.    
with app.app_context(): 
        db.create_all() #create the database tables based on MYTask class. If the tables already exist, this command will not overwrite them.

#homepage index.html
#POST AND GET METHODS: POST= SEND DATA FROM DATABASE TO HTML FILE , GET = GET DATA FROM HTML FILE TO DATABASE
@app.route("/",methods = ["POST", "GET"]) #to define a route for the root URL ("/") of the web application. When a user accesses the root URL, the index() function will be executed.
def index():
    #Add new Task : get from html file and add to database
    #by pressing submit in html and use post method, flask hold the request to python
    #if submit button is clicked in index.html, then the form data will be sent to the server ("/") using the POST method. The server will then process the data and add a new task to the database.
    if request.method == "POST":        
        content_task = request.form["content"] #read data from text input in html
        new_task = MyTask(content = content_task) #create a new instance of the MyTask class with the content_task value obtained from the HTML form. This represents a new task to be added to the database.
        try:
            db.session.add(new_task) #add without saving the new_task object to the database session. This prepares the object to be inserted into the database.
            db.session.commit() #save the changes to the database, which will insert the new task into the task table.    

            print(f"id: {new_task.id}, content: {new_task.content}, created: {new_task.created}") #print the id, content, and created timestamp of the newly added task to the console for debugging purposes.
            return redirect("/") #go back to html file: redirect the user back to the root URL ("/") after successfully adding the new task. This will trigger a GET request to the index() function, which will render the updated list of tasks.
        
        except Exception as e:
            #db.session.rollback()
            print(f"Error occurred while adding new task: {e}") #if an error occurs during the database operation, rollback the session to undo any changes made and print the error message for debugging purposes.    
            return f"There was an issue adding your task : {e}" #return an error message to the user if the task could not be added to the database.

    #show all current tasks in the database
    # if the submit btn not clicked in index.html, then show all tasks in the database, by default it will use GET method to retrieve data from the database and display it on the HTML page.
    else: 
        # tasks is a list of rows in the table_task, each row is an object of MyTask class. we can access the attributes of the object using dot notation. for example, to access the content of a task, we can use task.content.
        tasks = MyTask.query.order_by(MyTask.created).all() #query= select * from table_task order by created_at; retrieve all tasks from the database, ordered by their creation timestamp. The result is stored in the tasks variable, which will be passed to the HTML template for rendering.
        return render_template("index.html", tasks = tasks) #first tasks is a variable in index.html ,it holds all rows in database as list of objects; render the index.html template and pass the retrieved tasks as a variable named tasks. This allows the HTML template to access and display the list of tasks.
    
    #return render_template("index.html") #run the html file from template folder and display in web browser

#Delete an item from the database
#"/delete/<int:id>" : its a dummy path (url) just for refernce to know the kind of operation, ID is used for db to delete the item
#when click on delete link in index.html, the flask will call (delete(id:int) function) that has same route, it will call this function and pass the id of the task to be deleted as an argument. The function will then retrieve the corresponding task from the database using the provided ID, delete it from the database session, and commit the changes to permanently remove it from the database. Finally, it will redirect the user back to the root URL ("/") to display the updated list of tasks.
@app.route("/delete/<int:id>") # <int:id> is the id of the row : define a route for deleting a task based on its ID
def delete(id:int):
    task_to_delete = MyTask.query.get_or_404(id) #seearch by id in db:if found retrieve one row as object MyTask class, or return a 404 error if it doesn't exist.
    try:
        db.session.delete(task_to_delete) #remove the task from the database session.
        db.session.commit() #save the changes to the database.
        return redirect("/") #go back to index.html to update the table of task,redirect the user back to the root URL ("/") after successfully deleting the task.
    
    except Exception as e:
        print(f"Error occurred while deleting task: {e}") #if an error occurs during the database operation, print the error message for debugging purposes.
        return f"There was an issue deleting your task : {e}" #return an error message to the user if the task could not be deleted from the database.

#Update an item in the database
#in update.html, if you click submit, it post data in the input text field with post method in the form to the python code at @app.route("/update/<int:id>", methods = ["POST", "GET"]) def update(id:int): function
#the form in update.html post data to python and saved to db then redirect to (/)mean index.html,
# when click update link in index.html. it calls this function and redirect to update.html with the same data ,the form recive data (same data no change) by GET from else part of the function and display in the input text field for editing
#route path must be same as in update.html (<form action="/update/{{ task.id }}" method="POST">) in the form action, so that when the form is submitted, the request is sent to the correct route for processing. The <int:id> part of the route is a placeholder for the ID of the task to be updated, which will be passed as an argument to the update() function.

@app.route("/update/<int:id>", methods = ["POST", "GET"]) #define a route for updating a task based on its ID. This route accepts both POST and GET methods, allowing the user to retrieve the current task details for editing (GET) and submit the updated task details (POST).
def update(id:int):
    task = MyTask.query.get_or_404(id) #retrieve the task to be updated from the database using the provided ID. If the task does not exist, a 404 error will be returned.
    
    if request.method == "POST": #if the form is submitted (POST method), update the task's content with the new value from the HTML form and commit the changes to the database.
        task.content = request.form["content"] #update the content of the task with the new value obtained from the HTML form.
        try:
            db.session.commit() #save the changes to the database.
            return redirect("/") #go back to index.html to update the table of task,redirect the user back to the root URL ("/") after successfully updating the task.
        
        except Exception as e:
            print(f"Error occurred while updating task: {e}") #if an error occurs during the database operation, print the error message for debugging purposes.
            return f"There was an issue updating your task : {e}" #return an error message to the user if the task could not be updated in the database.

    else: #if it's a GET request (not active) from update.html or when click on Edit hyperlink in index.html, render the update.html template and pass the current task details for editing.
        return render_template("update.html", task = task) #the first variable is an object : task :hold one row in db, it is the same variable in update.html, to display the task in the browser for editing, render the update.html template and pass the current task details as a variable named task. This allows the HTML template to pre-fill the form with the existing task content for editing.





if __name__ == "__main__":
    
    app.run(debug=True)