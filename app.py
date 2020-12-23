import os
import random
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        # check if the username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("sign_up"))

        sign_in = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(sign_in)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Hi, {}. Welcome to books'world.".format(
                        request.form.get("username").capitalize()))
        flash("Click on the add button and create your fisrt book summary")
        return redirect(url_for(
            "profile", username=session["user"]))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid passwword match
                flash("Incorrect Username and/or Password")
                return render_template("login.html")

        else:
            # username does not exist
            flash("Incorrect Username and/or Password")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get the session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # get the session user's books from database
    books = list(mongo.db.books.find())
    quotes = mongo.db.quotes.aggregate([{"$sample": {"size": 1}}])
    # random_quote = range(0, quotes.length).random

    if session["user"]:
        return render_template(
            "profile.html", username=username, books=books, quotes=quotes)

    return redirect(url_for("login"))


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book = {
            "book_name": request.form.get("book_name"),
            "book_author": request.form.get("book_author"),
            "img_url": request.form.get("img_url"),
            "book_review": request.form.get("book_review"),
            "created_by": session["user"]
        }
        mongo.db.books.insert_one(book)
        return redirect("/profile/<username>")


@app.route("/view_book/<book_name>")
def view_book(book_name):
    book = mongo.db.books.find_one({"_id": ObjectId(book_name)})
    return render_template("view_book.html", book=book)


@app.route("/edit_book/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if request.method == "POST":
        edited_book = {
            "book_name": request.form.get("book_name"),
            "book_author": request.form.get("book_author"),
            "img_url": request.form.get("img_url"),
            "book_review": request.form.get("book_review"),
            "created_by": session["user"]
        }
        mongo.db.books.update({"_id": ObjectId(book_id)}, edited_book)

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("view_book.html", book=book)


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    mongo.db.books.remove({"_id": ObjectId(book_id)})
    return redirect("/profile/<username>")


@app.route("/best_books/<username>", methods=["GET", "POST"])
def best_books(username):
    # get the session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # get the session user's books from database
    book_lists = list(mongo.db.book_lists.find({'created_by': username}))

    if session["user"]:
        return render_template(
            "best_books.html", username=username, book_lists=book_lists)

    return redirect(url_for("login"))


@app.route("/add_list", methods=["GET", "POST"])
def add_list():
    if request.method == "POST":
        share_list = "on" if request.form.get("share_list") else "off"
        list = {
            "list_name": request.form.get("list_name"),
            "share_list": share_list,
            "created_by": session["user"],
            "books": []
        }
        mongo.db.book_lists.insert_one(list)
        return redirect("/best_books/<username>")


@app.route("/view_list/<list_name>")
def view_list(list_name):
    book_list = mongo.db.book_lists.find_one({"_id": ObjectId(list_name)})
    # list = mongo.db.book_lists.find_one(
    #     {"_id": ObjectId(list_name)})
    # CHECK IF I WILL USE IT AND DELETE THE PRINTS BELOW
    print(f"BOOK LIST: {book_list}")

    book_objects_list = []
    for book in book_list['books']:
        print(f"BOOK: {book}")
        book_item = mongo.db.books_in_list.find_one({'_id': ObjectId(book)})
        print(f"BOOK ITEM: {book_item}")
        book_objects_list.append(book_item)

    print(f"BOOK OBJECT LIST: {book_objects_list}")

    return render_template(
        "view_list.html", book_list=book_objects_list, list=book_list)


@app.route("/edit_list/<list_id>", methods=["GET", "POST"])
def edit_list(list_id):
    if request.method == "POST":
        share_list = "on" if request.form.get("share_list") else "off"

        mongo.db.book_lists.update_one(
            {"_id": ObjectId(
                list_id)}, {"$set": {"list_name": request.form.get(
                    "list_name"), "share_list": request.form.get(
                        "share_list")}})

    list = mongo.db.book_lists.find_one({"_id": ObjectId(list_id)})
    return redirect(url_for("view_list", list=list, list_name=list["_id"]))


@app.route("/delete_list/<list_id>")
def delete_list(list_id):
    mongo.db.book_lists.remove({"_id": ObjectId(list_id)})
    return redirect("/best_books/<username>")


@app.route("/add_book_in_list/<list_name>", methods=["GET", "POST"])
def add_book_in_list(list_name):
    if request.method == "POST":
        book = {
            "book_name": request.form.get("book_name"),
            "book_author": request.form.get("book_author"),
            "img_url": request.form.get("img_url"),
            "vendor_url": request.form.getlist("vendor_url"),
            "created_by": session["user"]
        }

        book_id = mongo.db.books_in_list.insert_one(book).inserted_id
        mongo.db.book_lists.update(
            {'_id': ObjectId(list_name)}, {'$push': {'books': book_id}})

        book_list = mongo.db.book_lists.find_one({"_id": ObjectId(list_name)})

    return redirect(url_for("view_list", list_name=book_list["_id"]))


@app.route("/book_info/<list_name>/<book_name>")
def book_info(list_name, book_name):
    # book_lists = list(mongo.db.book_lists.find())
    book = mongo.db.books_in_list.find_one({"_id": ObjectId(book_name)})
    book_list = mongo.db.book_lists.find_one({"_id": ObjectId(list_name)})
    return render_template("book_info.html", book=book, list=book_list)


@app.route("/edit_book_in_list/<list_name>/<book_id>", methods=["GET", "POST"])
def edit_book_in_list(list_name, book_id):
    if request.method == "POST":
        edited_book = {
            "book_name": request.form.get("book_name"),
            "book_author": request.form.get("book_author"),
            "img_url": request.form.get("img_url"),
            "vendor_url": request.form.getlist("vendor_url"),
            "created_by": session["user"]
        }
        mongo.db.books_in_list.update({"_id": ObjectId(book_id)}, edited_book)

    book = mongo.db.books_in_list.find_one({"_id": ObjectId(book_id)})
    book_list = mongo.db.book_lists.find_one({"_id": ObjectId(list_name)})
    return render_template("book_info.html", book=book, list=book_list)


@app.route("/delete_book_in_list/<list_name>/<book_id>")
def delete_book_in_list(list_name, book_id):
    book_list = mongo.db.book_lists.find_one({"_id": ObjectId(list_name)})

    mongo.db.books_in_list.remove({"_id": ObjectId(book_id)})
    mongo.db.book_lists.update(
            {'_id': ObjectId(
                list_name)}, {'$pull': {'books': ObjectId(book_id)}})
    return redirect(url_for("view_list", list_name=book_list["_id"]))


@app.route("/discover")
def discover():
    book_lists = list(mongo.db.book_lists.find())
    return render_template("discover.html", book_lists=book_lists)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    book_lists = list(mongo.db.book_lists.find({"$text": {"$search": query}}))
    return render_template("discover.html", book_lists=book_lists)


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("home"))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
