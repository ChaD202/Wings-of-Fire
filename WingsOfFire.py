from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def load(database):
    connection = sqlite3.connect(database)
    c = connection.cursor()

    posts = list(c.execute("SELECT * FROM Orders ORDER BY OrderID ASC"))  # converts into list instead of cursor object

    connection.close()

    return posts


def add(database, customer, address, meal, drink):
    connection = sqlite3.connect(database)
    c = connection.cursor()

    c.execute("INSERT INTO Orders (Customer, Address, Meal, Drink) VALUES ('{c}', '{a}', '{m}', '{d}')".format(
                c=customer, a=address, m=meal, d=drink))
    connection.commit()
    connection.close()


@app.route('/', methods=["GET", "POST"])
def start():
    db = "orders.db"
    if request.method == "GET":
        pass

    if request.method == "POST":  # if website gives data, add information to database
        name = request.form.get("name")
        address = request.form.get("address")
        meal = request.form.get("meal")
        drink = request.form.get("drink")

        add(db, name, address, meal, drink)

    return render_template("main.html")


@app.route('/kitchen')
def page():
    db = "orders.db"
    orders = load(db)
    return render_template("kitchen.html", orders=orders)
