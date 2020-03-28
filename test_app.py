import os
import pytest
import tempfile
from kanban import app, db

@pytest.fixture
def client():
    db_fd, url = tempfile.mkstemp()
    url = 'sqlite://' + url
    app.config['DATABASE'] = url
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Oops, you have no active tasks. Add tasks now!' in rv.data

def add(client,newtask_name,newtask_desc,newtask_status):
    return client.post('/add/',data=dict(
        newtask_name=newtask_name,
        newtask_desc=newtask_desc,
        newtask_status=newtask_status
    ), follow_redirects=True)

def test_add(client):
    rv = add(client,"task","task-desc","todo")
    assert b'Get started!' in rv.data

def update(client):
    return client.post('/update/1/', follow_redirects=True)

def test_update_todoing(client):
    rv = add(client,"task","task-desc","todo")
    rv = update(client)
    assert b'Done!' in rv.data

def test_update_todone(client):
    rv = add(client,"task","task-desc","doing")
    rv = update(client)
    assert b'Clear' in rv.data

def test_update_clear(client):
    rv = add(client,"task","task-desc","done")
    rv = update(client)
    assert b'task-desc' not in rv.data

if __name__ == '__main__':
    unittest.main()
