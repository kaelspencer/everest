from app import app
from flask import _app_ctx_stack
import MySQLdb

def get_db(app):
    top = _app_ctx_stack
    if not hasattr(top, 'mysql_db'):
        top.mysql_db = MySQLdb.connect(host=app.config['HOST'], user=app.config['USER'], passwd=app.config['PASSWORD'], db=app.config['DATABASE'])
    return top.mysql_db

@app.teardown_appcontext
def close_db(app):
    top = _app_ctx_stack.top
    if hasattr(top, 'mysql_db'):
        top.mysql_db.close()
