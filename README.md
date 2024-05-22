# Customer Ordering system Web app
# Designed for use by Alexander Ellis Furniture Emporium
#### A Web app for a furniture retail store to be used for Customer orders.
#### Video Demo:  <URL https://youtu.be/GNK88oQ1Em0>
## Overview

My web App is a versatile application designed to allow a furniture retail company to create customer orders. It is built using Python, for the main app, SQL for the database, accessed using sqlite3, jinja which links the html pages to the main layout, CSS (for the style and layout of the web pages) and flask as the Python web framework. This leverages several powerful libraries to provide a seamless and efficient user experience.

It contains the following files:-

 - The **Templates** folder:  
 html files for each page.

 - The **Static** folder   
 jpg images used throughout the app  
 The info page  
 The CSS files for making it all look pretty.

 - The <ins>**aepricelist.db**</ins> file
 This contains the database and is written in SQL.

 - The <ins>**extras.py**</ins> file
 This contains extra python script which is used within the python app.

 - The <ins>**app.py**</ins>
 This is the heart of the program which controls which page to show, makes the calculations required, and orders everything together. This is written in **Python**  

## Templates
Within the **Templates** folder, the following **html** files live, accessed through the **app.py**  


1. **layout.html**  
This is the template html file for all pages within the program. It allows the banner to be displayed atop of every page (unless specifically coded not to do so, in certain pages where it is not necessary). It also has a drop-down menu for registering a new user, and this encompasses the ability to add further pages as well.

2. **apology.html**  
This gives the user an apology for incorrect user details given, and shows an Error message, along with a description of what went wrong. (i.e. the wrong username, or password, or both)

3. **index.html**  
 This is the main home page of the app, where you are requested to log in, with no other access to the system at all.   
 From here you are taken to the   
 3a. **login.html** page.  
  This requests a username and password to be entered to gain access to the main home page, which keeps the site confidential.  

4.  **home.html**  
  This is the main confidential home page of the system. From here you can access the customer lists, current orders, current stock (both in the Bedroom range and the Lounge range).
  It is also possible to create a new customer, a new order, update a current order with a part or full payment, or add more items to a particular order.  
  There is also an option to set up a new user (staff member) to the system by using the drop-down menu atop the page.

## app.py
This is the main heart of the app. It is utilised via GET or POST requests from each of the html pages, either to display a particular page, or to (for example) utilise the database via SQL commands within the Python script, to calculate (eg the total cost of an order so far) and then display the relevant information on the requested page.



## To create a new customer the following html pages are utilised :-

- **Enter Customer Details**: Utilises `new_customer.html`.
- **Show List of all customers in the Database**: Utilises `list_of_customers.html`.
- **Create an order**: Utilises `customer_order.html` and `order_basics.html`.
- **To get a current Stock List**: Utilises `stock_list.html`.

## Installation

To install My Python App, you need to have Python 3.6+ installed on your machine. Follow the steps below:

1. Clone the repository:
    ```bash
    git clone https://github.com/matthewellwood/project-4.git
    ```
2. Navigate to the project directory:
    ```bash
    cd project-4
    ```


## Usage

To start using My App, follow these steps:

1. Run the main script:
    ```bash
    flask run
    ```
2. Follow the on-screen instructions to interact with the application.


