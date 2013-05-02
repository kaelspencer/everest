from app import app
from db import get_db, close_db

@app.route('/')
def hello():
    # get the db to execute code
    db = get_db(app)
    close_db(app)
    return 'Hello from controllers.py!\n'

@app.route('/jumps/<source>/<destination>/')
def jumps(source, destination):
    return 'Traveling from {} to {}\n'.format(source, destination)
