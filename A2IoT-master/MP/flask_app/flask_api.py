from flask import Flask, Blueprint, request, jsonify, render_template, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_site import home

"""
Custom api for the BELC Library Admin Dashboard System
"""

api = Blueprint("api", __name__)
db = SQLAlchemy()
ma = Marshmallow()


class Book(db.Model):
    """Model for table Book in MySQL DB"""
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.Text, unique=True)
    Author = db.Column(db.Text)
    PublishedDate = db.Column(db.Date)

    def __init__(self, Title, Author, PublishedDate, BookID=None):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate


class Admin(db.Model):
    """Model for admin table in MySQL DB"""
    __tablename__ = "Admins"
    adminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, unique=True)

    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password


class BookSchema(ma.Schema):

    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "PublishedDate")


class AdminSchema(ma.Schema):

    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        fields = ("adminID", "username", "password")


adminSchema = AdminSchema()
bookSchema = BookSchema()
booksSchema = BookSchema(many=True)


# Endpoint to show all books.
@api.route("/deletebook", methods=["GET"])
def get_books():
    books = Book.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)


# Endpoint to get book by id.
@api.route("/book/<id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id)

    return booksSchema.jsonify(book)


# Endpoint to create new book entry.
@api.route("/book", methods=["POST"])
def add_book():
    title = request.form["Title"]
    author = request.form["Author"]
    published_date = request.form["PublishedDate"]
    new_book = Book(Title=title, Author=author, PublishedDate=published_date)

    db.session.add(new_book)
    db.session.commit()
    message = "Book Added Successfully!"
    return render_template("addbook.html", message=message)

# Endpoint to delete book.
@api.route("/deletebook", methods=["POST"])
def delete_book():
    try:
        book_id = request.form["BookID"]
        book = Book.query.get(book_id)

        db.session.delete(book)
        db.session.commit()
        message = "Book Deleted Successfully!"
        response = requests.get("http://127.0.0.1:5000/deletebook")
        data = json.loads(response.text)
    except:
        response = requests.get("http://127.0.0.1:5000/deletebook")
        data = json.loads(response.text)
        message = "Can not delete borrowed book! Contact DB Administrator."
        return render_template("deletebook.html", books=data, message=message)
    return render_template("deletebook.html", books=data, message=message)

# Endpoint to retrieve and validate admin user
@api.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    query = db.session.query(Admin).filter(Admin.username.in_([POST_USERNAME]), Admin.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
        return render_template('adminHome.html')
    else:
        flash('wrong password!')
        return home()



