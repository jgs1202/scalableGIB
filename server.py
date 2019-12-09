# -*- coding: utf-8 -*-
# app.py
"""
 Using SQLAlchemy and Flask get db record.(GET)
"""
import os
from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from flaski.app import db, app
from flaski.app import Choice
from functools import wraps

# app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
# datasetpart = {}
# datasetparthourly = {}

@app.route("/")
def index():
    return "Hello World!"


def write(array):
    post = Choice(array[0], array[1], array[2], array[3], array[4], array[5], array[6], array[7], array[8], array[9], array[10])
    print(post, array)
    db.session.add(post)
    db.session.commit()


class Hello(Resource):
    def get(self, params):
        param = params.split('&')
        param = [p.split('=')[1] for p in param]
        # print(param)
        write(param)
        return param

api.add_resource(Hello, '/data/<params>')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='127.0.0.1', port=port)
