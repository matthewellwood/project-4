import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from extras import apology, login_required, GBP

# Configure application
app = Flask(__name__, static_folder='static')

# Custom filter
app.jinja_env.filters["GBP"] = GBP

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///aepricelist.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """Show Home Page"""
    # get things started
    if request.method == "POST":
        return render_template ("index.html")
    else:
        return render_template("index.html")


@app.route("/orders", methods=["GET", "POST"])
def orders():
    """Show order Page"""
    if request.method == "POST":
        return render_template ("orders.html")
    else:
        return render_template("orders.html")


@app.route("/list_of_orders", methods=["GET", "POST"])
def list_of_orders():
    # do this
    if request.method == "POST":
        # do this
        order_no = request.form.get("order_no")
        current = db.execute("SELECT * FROM orders WHERE order_no = (?);", order_no)
        for row in current:
            customer_id = row["cust_id"]
            staff_member = row["staff_member"]
            order_date = row["order_date"]
            #customer_last_name = row ["customer_last_name"]
            item_id = row["item_id"]
        #item_check = db.execute("SELECT Range, Style, selling_price FROM stock WHERE item_id = (?);", item_id)
        #for row in item_check:
            #name = row["Range"]
            #item_description = row["Style"]
            #selling_price = row["selling_price"]
        db.execute("INSERT INTO current_order(cust_id, staff_member, order_date, item_id, order_id) VALUES (?, ?, ?, ?, ?);", customer_id,  staff_member, order_date, item_id, order_no)
        return render_template("stock_list.html", order_no = order_no)
    else:
        ord_detail=db.execute("select * from orders;")
        #ord_detail = db.execute("select * from orders join customers on orders.cust_id = customers.id;")
        #return render_template("list_of_orders.html", ord_detail = ord_detail)
        return render_template("list_of_orders.html", ord_detail = ord_detail)


@app.route("/stock_list", methods=["GET", "POST"])
def stock_list():
        if request.method == "POST":
        # do this
            stock = db.execute("SELECT * FROM stock;")
            return render_template("stock_list.html")
        else:
            stock = db.execute("SELECT * FROM stock;")
            return render_template("stock_list.html", stock = stock)


@app.route("/lounge.html", methods=["GET", "POST"])
def lounge():
        if request.method == "POST":
        # do this
            return render_template("lounge.html")
        else:
            lounge = db.execute("SELECT * FROM stock WHERE Type = 'lounge' ;")
            return render_template("lounge.html", lounge = lounge)


@app.route("/bedroom.html", methods=["GET", "POST"])
def bedroom():
        if request.method == "POST":
        # do this
            bedroom = db.execute("SELECT * FROM stock WHERE Type = 'Bedroom' ;")
            return render_template("bedroom.html", bedroom = bedroom) 
            #return render_template("stock_list.html")
        else:
            bedroom = db.execute("SELECT * FROM stock WHERE Type = 'Bedroom' ;")
            return render_template("bedroom.html", bedroom = bedroom)
        

@app.route("/order_details", methods=["GET", "POST"])
def order_details():
    """Show Order Form"""
    if request.method == "POST":
        # do this
        order_number = request.form.get("order_number")
        quant = request.form.get("Quantity")
        if quant.isdigit():
            quantity = int(float(quant))
        item = request.form.get("item")
        if item.isdigit():
            item_id = int(float(item))
        item_check = db.execute("SELECT Range, Style, selling_price FROM stock WHERE item_id = (?);", item_id)
        for row in item_check:
            name = row["Range"]
            item_description = row["Style"]
            selling_price = row["selling_price"]
        #order_number = db.execute("SELECT order_no FROM orders ORDER BY order_no DESC LIMIT 1;")
        #for row in order_number:
            #current = row["order_no"]
            #current_order = int(current)
        #db.execute("INSERT INTO orders VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",'','',order_number,item_id,'','','','','', name, item_description,'', '', '', '', '', selling_price, '', quantity, '', '')
        #db.execute("INSERT INTO orders VALUES ('', '', '?','?', '', '', '', '', '',  '?', '?', '', '', '', '', '', '?', '', '?', '', '');",order_number,item_id, name, item_description, selling_price, quantity)
        db.execute("INSERT INTO orders VALUES item_id = (?), selling_price = (?), quantity = (?) order_no = (?);",item_id, selling_price, quantity, order_number)
        order_info = db.execute("SELECT * FROM orders WHERE order_id = (?);", order_number)
        return render_template("orders.html",order = order_info)
    else:
        ord_detail = db.execute("select staff_member, order_id, order_date, completion, orders.selling_price, delivery_date, stock.item_id, orders.item_name, address_3, postcode from orders join customers on orders.cust_id = customers.id join stock on orders.item_name = stock.item_name;")
        return render_template("list_of_orders.html", ord_detail = ord_detail)
    
    