from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def load(database, status):
    connection = sqlite3.connect(database)
    c = connection.cursor()

    if status == "all":
        # converts into list instead of cursor object and selects everything that hasn't been done in the kitchen
        posts = list(c.execute("SELECT * FROM Orders WHERE Done IS NOT 'Y' ORDER BY OrderID ASC"))

    else:
        # converts into list instead of cursor object, and ensures that the 'status' column is full
        posts = list(c.execute("SELECT * FROM Orders WHERE {s} IS NOT NULL ORDER BY OrderID ASC".
                               format(s=status.replace('"', ''))))

    connection.close()

    return posts


def add(database, customer, address, meal, drink, total):
    connection = sqlite3.connect(database)
    c = connection.cursor()

    c.execute("INSERT INTO Orders (Customer, Address, Meal, Drink, Price) VALUES ('{c}', '{a}', '{m}', '{d}', '£{p}')".
              format(c=customer, a=address, m=meal, d=drink, p=total))
    connection.commit()
    connection.close()


def status_update(database, status, orderid):
    connection = sqlite3.connect(database)
    c = connection.cursor()

    c.execute("UPDATE Orders SET {s}='Y' WHERE OrderID = {id}".
              format(id=orderid, s=status.replace('"', '')))
    connection.commit()


def remove(database, orderid):
    connection = sqlite3.connect(database)
    c = connection.cursor()

    c.execute("DELETE FROM Orders WHERE OrderID = {id}".
              format(id=orderid))
    connection.commit()


def price(meal, drink):
    prices = {"Lost In Spice": 1.00, "Henmageddon": 1.50, "A Cluck With Disaster": 2.50,
              "Coca Cola": 0.75, "Fanta": 0.80, "7UP": 1.00, "Flappucino": 1.50}

    total = prices[meal] + prices[drink]

    return total


@app.route('/', methods=["GET", "POST"])
def root():
    db = "orders.db"
    total = '{:.2f}'.format(0.00)
    if request.method == "GET":
        pass

    if request.method == "POST":  # if website gives data, add information to database
        name = request.form.get("name")
        address = request.form.get("address")
        meal = request.form.get("meal")
        drink = request.form.get("drink")
        total = '{:.2f}'.format(round(price(meal, drink), 2))

        add(db, name, address, meal, drink, total)

    return render_template("main.html", total=total)  # represents total with trailing zeros


@app.route('/kitchen', methods=["GET", "POST"])
def kitchen():
    db = "orders.db"
    orders = load(db, "all")

    if request.method == "POST":
        order_id = request.form.get("id")
        status_update(db, "Done", order_id)

    return render_template("kitchen.html", orders=orders)


@app.route('/delivery', methods=["GET", "POST"])
def delivery():
    db = "orders.db"
    orders = load(db, "Done")

    if request.method == "POST":
        order_id = request.form.get("id")
        remove(db, order_id)

    return render_template("delivery.html", orders=orders)
