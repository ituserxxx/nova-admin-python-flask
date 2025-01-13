from flask_sqlalchemy import SQLAlchemy

db = None
def db_init(app):
    global db
    db =  SQLAlchemy(app)
