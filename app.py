from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #instantiate Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/weiting/School/19-20/cs162/kanban/kanban.db'

db = SQLAlchemy(app) #instantiate SQLAlchemy

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    desc = db.Column(db.String,default='')
    status = db.Column(db.String, default='todo')

@app.route('/')
def index():
    todo = Tasks.query.filter_by(status='todo').all()
    doing = Tasks.query.filter_by(status='doing').all()
    done = Tasks.query.filter_by(status='done').all()
    return render_template('index.html', todo=todo, doing=doing, done=done)

@app.route('/add', methods=['POST'])
def add():
    newtask = Tasks(name=request.form['newtask'])
    db.session.add(newtask)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    id = request.form['updatebtn'] #id of item to be updated
    item = Tasks.query.filter_by(id=id).first() #find corresponding record
    print(item.status)
    if item.status == 'todo':
        item.status = 'doing'
    elif item.status == 'doing':
        item.status = 'done'
    else:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
