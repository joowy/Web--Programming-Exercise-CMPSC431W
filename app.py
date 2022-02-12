from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql


from livereload import Server


app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 7000


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/navigate", methods=["GET", "POST"])
# function used to navigate using drop down form.
def navigate():
    select = request.args.get("navigate")  # get value of form
    if select == "input":
        return redirect(url_for("input"))
    elif select == "delete":
        return redirect(url_for("delete"))
    return redirect(url_for("index"))


@app.route("/input", methods=["POST", "GET"])
def input():
    error = None
    if request.method == "POST":
        result = valid_name(request.form["FirstName"], request.form["LastName"])
        if result:
            return render_template("input.html", error=error, result=result)
        else:
            error = "invalid input name"
    return render_template("input.html", error=error)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    error = None
    if request.method == "POST":
        result = delete_patient(request.form["FirstName"], request.form["LastName"])
        if result:
            return render_template("delete.html", error=error, result=result)
        else:
            error = "invalid input name"
    return render_template("delete.html", error=error)


def valid_name(first_name, last_name):
    CONNECTION = sql.connect("database.db")
    CONNECTION.execute(
        "CREATE TABLE IF NOT EXISTS users (pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);"
    )
    CONNECTION.execute(
        "INSERT INTO users (firstname, lastname) VALUES (?,?);", (first_name, last_name)
    )
    CONNECTION.commit()
    cursor = CONNECTION.execute("SELECT * FROM users;")
    return cursor.fetchall()


def delete_patient(first_name, last_name):
    CONNECTION = sql.connect("database.db")
    CONNECTION.execute(
        "CREATE TABLE IF NOT EXISTS users (pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);"
    )
    CONNECTION.execute(
        "DELETE FROM users WHERE firstname=? and lastname=?;", (first_name, last_name)
    )
    CONNECTION.commit()
    cursor = CONNECTION.execute("SELECT * FROM users;")
    return cursor.fetchall()


if __name__ == "__main__":

    app.run(host=HOST, port=PORT, debug=True)
