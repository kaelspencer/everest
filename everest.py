from app import app
from db import close_db
from controllers import *

app.config.from_object('config')
app.config.from_envvar('EVEREST_CONFIG', silent=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
