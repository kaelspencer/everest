from app import app
from flask import _app_ctx_stack as stack
import MySQLdb

def get_db(app):
    top = stack.top
    if not hasattr(top, 'mysql_db'):
        top.mysql_db = MySQLdb.connect(host=app.config['HOST'], user=app.config['USER'], passwd=app.config['PASSWORD'], db=app.config['DATABASE'])
    return top.mysql_db

def close_db(app):
    top = stack.top
    if hasattr(top, 'mysql_db'):
        top.mysql_db.close()

# The db connection can timeout and a simply retry can fix it.
def try_execute(query, params):
    try:
        db = get_db(app)
        c = db.cursor()
        count = c.execute(query, params)
        return count, c
    except:
        app.logger.error('Exception thrown during execution. Retrying.')
        close_db(app)
        db = get_db(app)
        c = db.cursor()
        count = c.execute(query, params)
        return count, c

# Issues a query that is supposed to return exactly one row.
# LookupError exception is thrown if the query returns 0 items and a log warning
# is written if more than one is returned. In that case, the first row is returned.
def get_one(query, params):
    count, c = try_execute(query, params)

    if count == 0:
        app.logger.warning('No results returned for query <%s>, params <%s>' % (query, params))
        raise LookupError
    elif count > 1:
        app.logger.warning('Query count %d for query <%s>' % (count, query))

    return c.fetchone()

# Issues a query and returns all results.
def get_all(query, params):
    count, c = try_execute(query, params)
    return c.fetchall()
