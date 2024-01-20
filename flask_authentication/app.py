from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)
    # app.config.from_prefixed_env()
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config["SQLALCHEMY_ECHO"] = True
    # initialize exts
    db.init_app(app)

    return app