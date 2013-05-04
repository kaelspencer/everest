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

# Issues a query that is supposed to return exactly one row.
# LookupError exception is thrown if the query returns 0 items and a log warning
# is written if more than one is returned. In that case, the first row is returned.
def get_one(query, params):
    db = get_db(app)
    c = db.cursor()
    count = c.execute(query, params)

    if count == 0:
        raise LookupError
    elif count > 1:
        app.logger.warning('Query count %d for query <%s>' % (count, query))

    return c.fetchone()
