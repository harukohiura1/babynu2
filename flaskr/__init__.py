from flask import Flask
app = Flask(__name__)
import flaskr.main #main.pyのファイルのこと

from flaskr import db
db.create_tables()
