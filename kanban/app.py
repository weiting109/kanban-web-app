from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #instantiate Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #instantiate SQLAlchemy

class Tasks(db.Model): #create table using db.Model base class to store tasks
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    desc = db.Column(db.String,default='')
    status = db.Column(db.String, default='todo')

db.create_all() #create all tables

@app.route('/')
def index():
    """
    Render templates and display tasks according to status
    """
    ntasks = Tasks.query.count()
    todo = Tasks.query.filter_by(status='todo').all()
    doing = Tasks.query.filter_by(status='doing').all()
    done = Tasks.query.filter_by(status='done').all()
    return render_template('index.html', ntasks=ntasks,todo=todo, doing=doing, done=done)

@app.route('/add/', methods=['POST'])
def add():
    """
    Add a new task to the Kanban board (default status = todo)
    """
    newtask = Tasks(name=request.form['newtask_name'],desc=request.form['newtask_desc'], status=request.form['newtask_status'])
    db.session.add(newtask)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>/', methods=['POST'])
def update(id):
    """
    Update status of tasks to the next status in the following order: todo, doing, done.
    If task is done, update deletes the task from the board.
    """
    #id = request.form['updatebtn'] #id of item to be updated - no longer needed as id is passed through URL
    item = Tasks.query.filter_by(id=id).first() #find corresponding record
    if item.status == 'todo':
        item.status = 'doing'
    elif item.status == 'doing':
        item.status = 'done'
    else:
        #item.status='archived'
        #archived status for possible future expansion (undoing archive, for e.g./retrieving monthly report)
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
