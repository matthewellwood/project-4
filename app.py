import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp


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
    """Show Login Page"""
    # get things started
    #if request.method == "POST":
        #return render_template ("home.html")
    #else:
    """Log user in"""
    #Forget any user_id
    session.clear()
    #User reached route via POST 
    if request.method == "POST":
        # Get username 
        user = request.form.get("name")
        # Get a Password
        password = request.form.get("password")
        # Check Username is Valid
        valid = db.execute("SELECT * from USERS where username = (?);", user)
        for row in valid:
            pass_check = row["password"]
        # Check username exists and password is correct
            answer= "Wrong"
            if password == pass_check:
                answer = "Correct"
            if answer == "Correct":
                return render_template("home.html")
            #return render_template("test.html", answer=answer, pass_check=pass_check, password=password, user=user)
            #return render_template("test.html", pass_check=pass_check, password=password)
            #return render_template("home.html")
            #else:
                #return render_template("test.html", pass_check=pass_check, password=password)
                #return render_template("home.html")  
            return render_template("test.html", answer=answer, valid=valid, password=password, user=user)
    else:
        return render_template("index.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    """Show Home Page"""
    # get things started
    if request.method == "POST":
        return render_template ("home.html")
    else:
        return render_template("home.html")

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
        current = db.execute("SELECT * FROM orders WHERE order_id = (?);", order_no)
        for row in current:
            customer_id = row["cust_id"]
            staff_member = row["staff_member"]
            order_date = row["order_date"]
            item_id = row["item_id"]
        db.execute("INSERT INTO current_order(cust_id, staff_member, order_date, item_id, order_number) VALUES (?, ?, ?, ?, ?);", customer_id,  staff_member, order_date, item_id, order_no)
        return render_template("stock_list.html", order_no = order_no)
    else:
        order_no = request.form.get("order_no")
        totals=db.execute("select order_number, SUM(amount_paid) AS tot_paid FROM payments group by order_number;")
        for row in totals:
            order_numb = (row["order_number"])
            total = (row["tot_paid"])
            balance = (row["tot_paid"])
            db.execute("UPDATE current_order SET amount_paid = (?) WHERE order_number = (?);", total, order_numb)
        ord_detail = db.execute("select current_order.order_number, current_order.amount_paid, orders.staff_member, orders.cust_id, first_name, last_name, order_id,orders.order_date, orders.deposit, completion, orders.delivery_date, balance, total_cost from orders JOIN customers on orders.cust_id = customers.id JOIN current_order ON current_order.order_number = orders.order_id GROUP BY order_id;")
        for row in ord_detail:
            order_id = (row["order_id"])
            amount_paid = (row["amount_paid"])
            total_cost = (row["total_cost"])
            deposit = (row["deposit"])
            #bal = total_cost - deposit
            balance = total_cost - deposit- amount_paid
            db.execute("UPDATE orders SET balance = (?) WHERE order_id = (?);", balance, order_id)
        finals = db.execute("select current_order.order_number, current_order.amount_paid, orders.staff_member, orders.cust_id, balance, first_name, last_name, order_id,orders.order_date, orders.deposit, completion, orders.delivery_date, balance, total_cost from orders JOIN customers on orders.cust_id = customers.id JOIN current_order ON current_order.order_number = orders.order_id GROUP BY order_id;")
        return render_template("open_orders.html", ord_detail = finals)


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
    

@app.route("/add_to_order", methods=["GET", "POST"])
def add_to_order():
    """Show Order Form"""
    if request.method == "POST":
        order_cost = 0.00
        order_no = request.form.get("order_no")
        item_id = request.form.get("item_id")
        quantity = request.form.get("Quantity")
        get_cust = db.execute("Select cust_id FROM orders WHERE order_id = (?);", order_no)
        for cust in get_cust:
            customer_id = cust["cust_id"]
            db.execute("UPDATE current_order SET cust_id = (?) WHERE order_number = (?);", customer_id, order_no)
        get_details = db.execute("SELECT selling_price FROM stock WHERE item_id = (?);", item_id)
        for row in get_details:
            selling_price = row["selling_price"]
            db.execute("INSERT INTO current_order (item_id, selling_price, quantity, order_number) VALUES (?, ?, ?, ?);",item_id, selling_price, quantity, order_no)
        current = db.execute("SELECT * FROM current_order JOIN stock ON current_order.item_id = stock.item_id WHERE order_number = (?);", order_no)
        tot = float(0.00)
        for row in current:
            sell = float(row["selling_price"])
            quant = int(quantity)
            total = (quant * sell)
            tot += (total)
            line_tot = (quant * sell)
            order_cost += line_tot
            db.execute("UPDATE current_order SET total_cost = (?) WHERE order_number = (?);", order_cost, order_no)
        return render_template("current_order.html",current = current,order_number = order_no, total_cost = order_cost)
    else:
        # If GET 
        return render_template("stock_list.html")


@app.route("/save_current", methods=["GET", "POST"])
def save_current():
    """Show order Page"""
    if request.method == "POST":
        order_no = request.form.get("order_no")
        total_order_cost = request.form.get("total_cost")
        #current = db.execute ("SELECT current_order.item_id, stock.selling_price, current_order.Quantity FROM current_order JOIN orders on current_order.order_number = orders.order_id JOIN stock ON current_order.item_id = stock.item_id;")
        #tot = float(0.00)
        db.execute("UPDATE orders SET balance = (?) WHERE order_id =(?);", total_order_cost, order_no)
        totals=db.execute("select order_number, SUM(amount_paid) AS tot_paid FROM payments WHERE order_number = (?);", order_no)
        for row in totals:
            total_paid = (row["tot_paid"]) 
        finals = db.execute("select current_order.order_number, current_order.amount_paid, orders.staff_member, orders.cust_id, balance, first_name, last_name, order_id,orders.order_date, orders.deposit, completion, orders.delivery_date, balance, total_cost from orders JOIN customers on orders.cust_id = customers.id JOIN current_order ON current_order.order_number = orders.order_id GROUP BY order_id;")
        return render_template("open_orders.html", total_paid = total_paid, ord_detail = finals)
    else:
        ord_detail = db.execute("select orders.staff_member, orders.cust_id, last_name, order_id,orders.order_date, orders.deposit, completion, orders.delivery_date, balance, total_cost from orders JOIN customers on orders.cust_id = customers.id JOIN current_order ON current_order.order_number = orders.order_id GROUP BY order_id;")
        for name in ord_detail:
            last_name = name["last_name"]
        return render_template("orders.html", last_name = last_name)


@app.route("/show_content", methods=["GET", "POST"])
def show_content():
    """Show order contents Page"""
    if request.method == "POST":
        order_number = request.form.get("order_no")
        detail = db.execute("SELECT * FROM current_order JOIN stock ON current_order.item_id = stock.item_id JOIN orders ON current_order.order_number = orders.order_id JOIN customers ON customers.id = orders.cust_id WHERE order_number = (?)  ;", order_number)
        for row in detail:
            total_cost = row["total_cost"]
            first_name = row["first_name"]
            last_name = row["last_name"]
            delivery_date = row["delivery_date"]
            staff_member = row["staff_member"]
        items = db.execute("select orders.staff_member, orders.order_date, sum(current_order.Quantity) AS Quanities,current_order.item_id, Name, Description, stock.selling_price FROM current_order JOIN stock on current_order.item_id = stock.item_id JOIN orders ON current_order.order_number = orders.order_id WHERE order_number = (?) group by stock.item_id;", order_number)
        return render_template("order_contents.html",ord_detail = detail, staff_member = staff_member, customer_first = first_name, customer_name = last_name, order_number = order_number,total_cost = total_cost, delivery_date = delivery_date, items = items)
    else:
        order_number = request.form.get("order_no")
        detail = db.execute("SELECT * FROM current_order WHERE order_number = (?);", order_number)
        return render_template("order_contents.html",ord_detail = detail, items = items)
    

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
        customer_id = request.form.get("customer_id")
        staff_member = request.form.get("staff_member")
        order_date = request.form.get("order_date")
        deposit = request.form.get("deposit_taken")
        deposit = float(deposit)
        db.execute("INSERT INTO orders(cust_id, staff_member, order_date, deposit, amount_paid) VALUES (?, ?, ?, ?, 0);", customer_id,  staff_member, order_date, deposit)
        order_info = db.execute("SELECT * FROM orders order by order_id desc limit 1;")
        for row in order_info:
            last_elem = row["order_id"]
        return render_template("order_basics.html", last_elem = last_elem)
    else:
        return render_template("customer_order.html")


@app.route("/order_basics", methods=["GET", "POST"])
def order_basics():
    # things to change
    if request.method == "POST":
        order_no = request.form.get("order_no")
        completion = request.form.get("completion")
        del_date = request.form.get("delivery_date")
        db.execute("UPDATE orders SET completion = (?), delivery_date = (?) WHERE order_id =(?);", completion, del_date, order_no)
        return render_template("stock_list.html", order_no = order_no)
    else:
        current_order_no = db.execute("SELECT order_id FROM orders ORDER BY order_id desc LIMIT 1;")
        for row in current_order_no:
            order_number = (row["order_id"])
        return render_template("order_basics.html",  order_number = order_number) 
    

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
        ord_detail = db.execute("select orders.staff_member, orders.cust_id, last_name, order_id,orders.order_date, orders.deposit, completion, orders.delivery_date, balance, total_cost from orders JOIN customers on orders.cust_id = customers.id JOIN current_order ON current_order.order_number = orders.order_id GROUP BY order_id;")
        return render_template("payments.html", payments =  ord_detail)
    else:
        ord_detail = db.execute("select orders.staff_member, orders.cust_id, last_name, order_id,orders.order_date, orders.deposit, completion, orders.delivery_date, balance, total_cost from orders JOIN customers on orders.cust_id = customers.id JOIN current_order ON current_order.order_number = orders.order_id GROUP BY order_id;")
        return render_template("payments.html", payments =  ord_detail)


@app.route("/pay", methods =["GET","POST"])
def pay():
    """Show Payments screen"""
    if request.method == "POST":
        order_number = request.form.get("order_no")
        name = db.execute("SELECT first_name, last_name FROM customers JOIN orders on orders.cust_id = customers.id where orders.order_id = (?);", order_number)
        for row in name:
            first_name = (row["first_name"])
            last_name = (row["last_name"])
        return render_template("pay.html", order_number = order_number, first_name = first_name, last_name = last_name )
    else:
        order_number = request.form.get("order_no")
        return render_template("pay.html", order_number = order_number)

@app.route("/paid", methods =["GET","POST"])
def paid():
    if request.method == "POST":
        order_number = request.form.get("order_no")
        amount_paid = request.form.get("paid_amount")
        paid_date = request.form.get("paid_date")
        check = db.execute("SELECT * FROM payments")
        #for row in check:
            #order_check = (row["order_number"])
        if order_number in check:
            db.execute("INSERT INTO payments (amount_paid, date_paid) VALUES (?, ?) WHERE order_number = (?);", amount_paid, paid_date, order_number)
        else:
            db.execute("INSERT INTO payments (amount_paid, date_paid, order_number) VALUES (?, ?, ?);", amount_paid, paid_date, order_number)
        taken=db.execute("select payments.amount_paid, payments.date_paid, current_order.total_cost, orders.deposit from payments join current_order on current_order.order_number=payments.order_number JOIN orders on orders.order_id = payments.order_number JOIN customers on orders.cust_id = customers.id WHERE payments.order_number = (?) GROUP BY date_paid;", order_number)
        for row in taken:
            total_cost = (row["total_cost"])
        payments=db.execute("select order_number, SUM(amount_paid) AS tot_paid FROM payments WHERE order_number = (?);", order_number)
        totals=db.execute("SELECT SUM(payments.amount_paid) AS total_paid, orders.deposit, current_order.total_cost from payments JOIN current_order ON current_order.order_number=payments.order_number JOIN orders ON orders.order_id = payments.order_number where payments.order_number=(?);", order_number)
        for row in payments:
            total_paid = (row["tot_paid"])
        return render_template("payments_taken.html", payments = payments, totals = totals, total_cost = total_cost, order_number = order_number, total_paid = total_paid)
    else:
        return render_template("payments_taken.html")


@app.route("/itemised_payments", methods =["GET","POST"])
def itemised_payments():
    if request.method == "POST":
        order_number = request.form.get("order_no")
        paid=db.execute("select id, date_paid, amount_paid FROM payments WHERE order_number = (?);", order_number)
        totals=db.execute("select order_number, SUM(amount_paid) AS tot_paid FROM payments WHERE order_number = (?);", order_number)
        for row in totals:
            total_paid = (row["tot_paid"])              
        return render_template("itemised_payments.html", paid = paid, order_number = order_number, total_paid = total_paid)
    

@app.route("/choose_customer", methods=["GET", "POST"])
def choose_customer():
    if request.method == "POST":
        selection = request.form.get("customer")
    else:
        return render_template("choose_customer.html")
