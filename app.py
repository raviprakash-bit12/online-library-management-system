from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask,render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            return "Login Successful!"
        else:
            return "Invalid Credentials"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])


        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"].strip().lower()
        author = request.form["author"].strip().lower()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Check if book already exists
        cursor.execute(
            "SELECT * FROM books WHERE title=? AND author=?",
            (title, author)
        )
        book = cursor.fetchone()

        if book:
            conn.close()
            return "This book already exists in the library."

        # Insert new book
        cursor.execute(
            "INSERT INTO books (title, author, available) VALUES (?, ?, ?)",
            (title, author, 1)
        )

        conn.commit()
        conn.close()

        return "Book Added Successfully"

    return render_template("add_book.html")


@app.route("/books")
def books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    return render_template("books.html", books=books)


@app.route("/borrow/<int:book_id>")
def borrow(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return redirect("/books")

@app.route("/return/<int:book_id>")
def return_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    return redirect("/books")




if __name__ == "__main__":
    app.run(debug=True)

