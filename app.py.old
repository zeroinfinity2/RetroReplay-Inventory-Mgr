import segno
from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
import sqlite3
import os
from werkzeug.utils import secure_filename
import datetime

# IMPORTANT STUFF --------------------------------------
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '1d5db266e7902199cc6cb39e6511cd81ccd9da827fa9deaf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ------------------------------------------------------


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    conn = get_db_connection()
    # Grab the console counts
    consoles = conn.execute('SELECT COUNT(*) FROM Products INNER JOIN Consoles ON Products.ProductCode = Consoles.ProductCode').fetchone()
    # Grab recents added items
    recent_added = conn.execute('SELECT * FROM Products ORDER BY Products.ProductID DESC LIMIT 5').fetchall()
    conn.close()
    return render_template('index.html', consoles=consoles, recent=recent_added)


@app.route('/item/<itemcode>', methods=('GET', 'POST'))
def item(itemcode):
    code = f'{escape(itemcode)}'
    # Establish a connection
    conn = get_db_connection()

    # If the item sold returns the proper value (1)
    if request.form.get("itemsold"):
        # Get the sale status.
        sale_status = request.form['itemsold']

        # Connect to the DB and save the changes.
        conn.execute(f"UPDATE Products SET ProductSold = {sale_status} WHERE ProductCode = '{code}'")
        conn.commit()
        flash("Item marked as sold.")

    # If modifications were made to mods
    if request.form.get("mods"):
        # Get the mods changes
        mods = request.form['mods']

        # Connect to the DB and save the changes.
        conn.execute(f"UPDATE Consoles SET ConsoleMods = '{mods}' WHERE ProductCode = '{code}'")
        conn.commit()

    # If request to delete item was made
    if request.form.get("delete"):
        # Delete from the database
        conn.execute(f"DELETE FROM Products WHERE ProductCode = '{code}'")
        conn.execute(f"DELETE FROM Consoles WHERE ProductCode = '{code}'")
        conn.commit()
        conn.close()
        # Delete the QR code file
        if os.path.exists(f"static/qrcodes/{code}.png"):
            os.remove(f"static/qrcodes/{code}.png")
        # Go back to index after delete
        flash("Item successfully removed from the database.")
        return redirect(url_for('index'))

    # Show the item

    # Find the result if it exists.
    # FIXME: This only searches for consoles. Update this to search all products.
    result = conn.execute(f"SELECT * FROM Products LEFT JOIN Consoles ON Products.ProductCode = Consoles.ProductCode WHERE Consoles.ProductCode = '{code}'").fetchall()
    conn.close()
    return render_template('item.html', result=result)


@app.route('/addconsole/', methods=('GET', 'POST'))
def addconsole():
    conn = get_db_connection()
    # Grab all of the console codes
    consoles = conn.execute('SELECT * FROM ConsoleTypes').fetchall()
    conn.close()

    if request.method == 'POST':
        console_code = request.form['nameoptions']
        console_model = request.form['model']
        console_board = request.form['board']
        console_mods = request.form['mods']
        cost = request.form['cost']
        '''
        Types:
        1: Console
        2: Mod
        3: Capkit
        99: Other
        '''
        # FIXME: Change add console to add product, expand functionality to add different types of products.
        # For now, consoles are hardcoded.
        product_type = 1
        if not console_code:
            flash('Console is required!')
        elif not console_model:
            flash('Model is required!')
        elif not console_board:
            flash('Board Revision is required!')
        elif not cost:
            flash('Cost is required. Type 0 for free.')
        else:
            # If a console is being added, find the console's name and image based on the selected console code
            for console in consoles:
                if console['ConsoleCode'] == console_code:
                    console_name = console['ConsoleName']

            # Generate the in-date
            sys_indate = datetime.datetime.now().strftime("%m%d%Y%H%M%S")

            # Generate Product Code
            product_code = create_product_code(console_code, product_type, sys_indate)

            # Create the QR Code
            create_QR(product_code)

            conn = get_db_connection()
            conn.execute('INSERT INTO Products (ProductName, ProductIdentifier, Indate, ProductType, ProductCost, ProductCode) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (console_name, console_code, sys_indate, product_type, cost, product_code))
            conn.commit()
            conn.execute('INSERT INTO Consoles (ConsoleMods, ConsoleModel, ConsoleBoard, ProductCode, ConsoleCode) VALUES (?, ?, ?, ?, ?)',
                         (console_mods, console_model, console_board, product_code, console_code))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('addconsole.html', console_names=consoles)


@app.route('/search/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        query = request.form['query']
        return redirect(f"/item/{query}")
    return render_template('search.html')


@app.route('/add_console_type/', methods=('GET', 'POST'))
def add_console_type():
    if request.method == 'POST':
        # Case if there's no image
        if 'image' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['image']

        # If the filename is blank
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        # If the file exists and is an allowed filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Before saving the file, make sure there is valid name input
            name = request.form['console_name']
            console_code = request.form['console_code']

            if not name:
                flash('Name is required!')
            else:
                # Rename the filename to the codename of the console "CODE.PNG"
                filename = f"{console_code}.{filename.rsplit('.')[1].lower()}"

                # Add the new console type and save the image
                conn = get_db_connection()
                conn.execute(f"INSERT INTO ConsoleTypes (ConsoleName, ImgFile, ConsoleCode) VALUES ('{name}', '{filename}', '{console_code}')")
                conn.commit()
                conn.close()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash(f'Console {name} successfully added.')
            return redirect(request.url)

    return render_template('add_console_type.html')


def create_product_code(product_code, product_type, indate):
    """Creates product codes based on the unique info.
    """
    return f"{product_code}{product_type}{indate}"


def create_QR(product_code):
    '''Creates a QR Code for easy access.
    '''
    qrcode = segno.make(f'{product_code}')
    qrcode.save(f'./static/qrcodes/{product_code}.png', light='lightblue', scale='10')
