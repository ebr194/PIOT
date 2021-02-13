from flask import Flask, Blueprint, request, jsonify, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

"""
BELC Library System site routes
"""

site = Blueprint("site", __name__)


@site.route("/add_book")
def add_book():
    return render_template("addbook.html")


@site.route("/delete_book")
def delete_book():
    response = requests.get("http://127.0.0.1:5000/deletebook")
    data = json.loads(response.text)

    return render_template("deletebook.html", books=data)


@site.route("/admin_dashboard")
def index():
    return render_template("adminHome.html")


@site.route("/get_stats")
def get_graphs():
    return render_template("statistics.html")


@site.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("adminHome.html")


@site.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

