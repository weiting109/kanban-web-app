# Kanban Web app

## Author
Wei-Ting Yap

## About the project
Basic Kanban web app that allows any user to:
- Add new task (name, description, status)
- Update the status of a task (to-do, doing or done)
- Delete tasks ('Clear' once done)

It also alerts the user to create a new task if there are none active on the Kanban dashboard.

## Project structure
The app is created with the Flask microframework, using flask_sqlalchemy's abstraction to deal with databases, and HTML and CSS for styling with the help of Bootstrap.

## Instructions

###To run the app:
`
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ export FLASK_APP=kanban
$ flask run
`

###To test the app:
`
$ pytest
`
