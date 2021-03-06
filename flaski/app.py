from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(40), unique=False)
    username = db.Column(db.String(40), unique=False)
    gender = db.Column(db.String(80), unique=False)
    age = db.Column(db.String(20), unique=False)
    layout = db.Column(db.String(20), unique=False)
    level = db.Column(db.String(20), unique=False)
    node_history = db.Column(db.String(160), unique=False)
    path = db.Column(db.String(80), unique=False)
    path_length_difference = db.Column(db.String(20), unique=False)
    groupSize = db.Column(db.String(10), unique=False)
    origin_file = db.Column(db.String(80), unique=False)
    file = db.Column(db.String(80), unique=False)
    answer = db.Column(db.String(80), unique=False)
    time = db.Column(db.String(80), unique=False)
    # choice2 = db.Column(db.String(80), unique=False)

    def __init__(self, date, username, gender, age, layout, level, node_history, path, path_length_difference, groupSize, origin_file, file, answer, time):
        self.date = date
        self.username = username
        self.gender = gender
        self.age = age
        self.layout = layout
        self.level = level
        self.node_history = node_history
        self.path = path
        self.path_length_difference = path_length_difference
        self.groupSize = groupSize
        self.origin_file = origin_file
        self.file = file
        self.answer = answer
        self.time = time
        # self.choice2 = choice2

    def __repr__(self):
        return '<User %r>' % self.username
