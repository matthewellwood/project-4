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


@app.route("/open_orders", methods=["GET", "POST"])
def open_orders():
    # do this
    if request.method == "POST":
        # do this
        order_no = request.form.get("order_no")
        current = db.execute("SELECT * FROM orders WHERE order_no = (?);", order_no)
        for row in current:
            customer_id = row["cust_id"]
            staff_member = row["staff_member"]
            order_date = row["order_date"]
            item_id = row["item_id"]
        db.execute("INSERT INTO current_order(cust_id, staff_member, order_date, item_id, order_number) VALUES (?, ?, ?, ?, ?);", customer_id,  staff_member, order_date, item_id, order_no)
        return render_template("stock_list.html", order_no = order_no)
    else:
        ord_detail=db.execute("select * from orders join customers on orders.cust_id = customers.id;")
        #order_detail = ("select * from customers as c join current_order as co on c.id = co.cust_id join orders as o on o.order_no = co.cust_id;")
        return render_template("open_orders.html", ord_detail = ord_detail)


@app.route("/stock_list", methods=["GET", "POST"])
def stock_list():
        if request.method == "POST":
        # do this
            order_no = request.form.get("order_no")
            stock = db.execute("SELECT * FROM stock ;")
            return render_template("stock_list.html",order_no = order_no)
        else:
            order_no = request.form.get("order_no")
            stock = db.execute("SELECT * FROM stock;")
            return render_template("stock_list.html", stock = stock, order_no = order_no)


@app.route("/lounge", methods=["GET", "POST"])
def lounge():
        if request.method == "POST":
        # do this
            order_no = request.form.get("order_no")
            lounge = db.execute("SELECT * FROM stock WHERE Range = 'lounge' ;")
            return render_template("lounge.html", lounge = lounge, order_no = order_no)
         
        else:
            lounge = db.execute("SELECT * FROM stock WHERE Range = 'lounge' ;")
            return render_template("lounge.html", lounge = lounge)


@app.route("/bedroom", methods=["GET", "POST"])
def bedroom():
        if request.method == "POST":
        # do this
            order_no = request.form.get("order_no")
            bedroom = db.execute("SELECT * FROM stock WHERE Range = 'Bedroom' ;")
            return render_template("bedroom.html", bedroom = bedroom, order_no = order_no) 
        else:
            bedroom = db.execute("SELECT * FROM stock WHERE Range = 'Bedroom' ;")
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
            # name = row["Range"]
            #item_description = row["Style"]
            selling_price = row["selling_price"]
        db.execute("INSERT INTO orders (item_id, selling_price, quantity, order_no) VALUES (?, ?, ?, ?);",item_id, selling_price, quantity, order_number)
        order_info = db.execute("SELECT * FROM orders WHERE order_id = (?);", order_number)
        return render_template("orders.html",order = order_info)
    else:
        ord_detail = db.execute("select staff_member, order_id, order_date, completion, orders.selling_price, delivery_date, stock.item_id, orders.item_name, address_3, postcode from orders join customers on orders.cust_id = customers.id join stock on orders.item_name = stock.item_name;")
        return render_template("order_contents.html", ord_detail = ord_detail)
    

@app.route("/add_to_order", methods=["GET", "POST"])
def current_orders():
    """Show Order Form"""
    if request.method == "POST":
        order_no = request.form.get("order_no")
        item_id = request.form.get("item_id")
        quantity = request.form.get("Quantity")
        get_details = db.execute("SELECT selling_price FROM stock WHERE item_id = (?);", item_id)
        for row in get_details:
            selling_price = row["selling_price"]
        # USE PYTHON TRY ?????
        check_order = db.execute("SELECT item_id FROM current_order WHERE order_number = (?);", order_no)
        for row in check_order:
            item = row["item_id"]
            #if item_id = item:
                # UPDATE QUANTITY OF ITEM IN CURRENT ORDER , ELSE INSERT ITEM INTO ORDER
        db.execute("INSERT INTO current_order (item_id, selling_price, quantity, order_number) VALUES (?, ?, ?, ?);",item_id, selling_price, quantity, order_no)
        current = db.execute("SELECT * FROM current_order JOIN stock ON current_order.item_id = stock.item_id WHERE order_number = (?);", order_no)
        tot = float(0.00)
        for row in current:
            sell = float(row["selling_price"])
            quant = float(quantity)
            total = float(quant * sell)
            tot += float(total)
        return render_template("current_order.html",current = current,order_number = order_no, total_cost = tot)
    else:
        # do the other
        return render_template("stock_list.html")


@app.route("/save_current", methods=["GET", "POST"])
def save_current():
    """Show order Page"""
    if request.method == "POST":
        order_no = request.form.get("order_no")
        total = request.form.get("total_cost")
        db.execute("UPDATE orders SET balance = (?) WHERE order_no =(?);", total, order_no)
        totals = db.execute("SELECT order_number, total_cost FROM current_order;")
        ord_detail=db.execute("select * from orders;")
        return render_template("open_orders.html", ord_detail = ord_detail)
    else:
        return render_template("orders.html")


@app.route("/show_content", methods=["GET", "POST"])
def show_content():
    """Show order Page"""
    if request.method == "POST":
        order_number = request.form.get("order_no")
        detail = db.execute("SELECT * FROM current_order JOIN stock ON current_order.item_id = stock.item_id WHERE order_number = (?)  ;", order_number)
        return render_template("order_contents.html",ord_detail = detail, order_number = order_number)
    else:
        order_number = request.form.get("order_no")
        detail = db.execute("SELECT * FROM current_order WHERE order_number = (?);", order_number)
        return render_template("order_contents.html",ord_detail = detail)
    
@app.route("/list_of_customers", methods=["GET", "POST"])
def list_of_customers():
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        detail = db.execute("select * from customers WHERE id = (?);", customer_id)
        return render_template("customer_order.html",customer_id = customer_id, detail = detail)
    else:
        detail = db.execute("select * from customers;")
        return render_template("list_of_customers.html",detail = detail)


@app.route("/customer_order", methods=["GET", "POST"])
def customer_order():
    """Show Order Form"""
    if request.method == "POST":
        staff_member = request.form.get("staff_member")
        order_date = request.form.get("order_date")
        customer_id = request.form.get("customer_id")
        deposit = request.form.get("deposit_taken")
        #customer = db.execute ("SELECT * FROM customers WHERE id = (?);", customer_id)
        db.execute("INSERT INTO orders(cust_id, staff_member, order_date, deposit) VALUES (?, ?, ?, ?);", customer_id,  staff_member, order_date, deposit)
        order_info = db.execute("SELECT * FROM orders;")
        last_elem =order_info[len(order_info)-1]
        return render_template("order_basics.html", last_elem = last_elem)
    else:
        return render_template("customer_order.html")


@app.route("/order_basics", methods=["GET", "POST"])
def order_basics():
    # things to change
    if request.method == "POST":
        order_info = db.execute("SELECT * FROM orders;")
        last_elem =order_info[len(order_info)-1]
        return render_template("stock_list.html", last_elem = last_elem)
    else:
        return render_template("order_basics.html") 
    

@app.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    """Show Order Form"""
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        address_1 = request.form.get("Address_1")
        address_2 = request.form.get("Address_2")
        address_3 = request.form.get("Address_3")
        postcode = request.form.get("Postcode")
        telephone_1 = request.form.get("Telephone_1")
        telephone_2 = request.form.get("Telephone_2")
        db.execute("INSERT INTO customers(first_name, last_name, address_1, address_2, address_3, postcode, telephone_1, telephone_2) VALUES (?,?,?,?,?,?,?,?);", first_name, last_name, address_1, address_2, address_3, postcode, telephone_1, telephone_2 ) 
        detail = db.execute("select * from customers;")
        return render_template("list_of_customers.html",detail = detail)
    if request.method == "GET":
        return render_template("new_customer.html")


@app.route("/payments", methods=["GET", "POST"])
def payments():
    """Show Order Form"""
    if request.method == "POST":
        order_number = request.form.get("order_no")
        #payments = db.execute("SELECT * FROM customers AS c JOIN current_order AS co ON c.id = co.cust_id JOIN orders AS o ON o.cust_id = c.id WHERE co.order_number = (?);", order_number)
        payment2 = db.execute("SELECT * FROM orders WHERE order_no = (?);", order_number)
        #pay3 = db.execute("SELECT * FROM orders JOIN stock ON orders.item_id = stock.item_id WHERE order_number = (?);", order_number)
        tot = float(0.00)
        for row in payment2:
            balance = float(row["balance"])
            deposit = float("deposit")
            total = float(balance - deposit)
            tot += float(total)

        #outstanding = float(0.00)
        #for row in payment2:
         #   total = row["balance"]
          #  paid = row["deposit"]
           # outstanding = (total-paid)
        return render_template("payments.html", payments = payment2, outstanding = tot)
    else:
        return render_template("payments.html")
    

@app.route("/choose_customer", methods=["GET", "POST"])
def choose_customer():
    if request.method == "POST":
        selection = request.form.get("customer")
    else:
        return render_template("choose_customer.html")
