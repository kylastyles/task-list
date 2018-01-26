# <------------------------------------ SETUP ------------------------------------------->
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:***@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# <---------------------------------- CLASSES ----------------------------------------->
class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

# <------------------------------------- ROUTES --------------------------------------->
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    
    encouragement = ["Congratulations on staying organized!", "You Can Do It!", 
    "You've got this!", "Where there's a will, there's a way."]
    num = random.randint(0,3)
    message = encouragement[num]

    return render_template('todos.html',title='Get It Done!', tasks=tasks, 
    completed_tasks=completed_tasks, message=message)

@app.route('/delete-task', methods=['POST'])
def delete_task():
    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.run()
