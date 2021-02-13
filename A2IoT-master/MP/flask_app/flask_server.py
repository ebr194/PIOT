from flask import Flask, request, redirect, jsonify, render_template, session, url_for, flash
import os
from flask_api import *
from flask_site import *
"""
Flask app settings and service initialization
"""

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Update HOST and PASSWORD appropriately.
HOST = "35.201.3.196"
USER = "root"
PASSWORD = "password"
DATABASE = "iotA2"

app.config['SECRET_KEY'] = '123456790'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)
app.register_blueprint(api)
app.register_blueprint(site)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
