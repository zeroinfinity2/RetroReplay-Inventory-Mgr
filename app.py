import segno
from flask import Flask, render_template, request, url_for, flash, redirect
from console import Console
from markupsafe import escape
import sqlite3
import os
from werkzeug.utils import secure_filename

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
    # Grab the counts
    consoles = conn.execute('SELECT COUNT(*) FROM Products INNER JOIN Consoles ON Products.ProductCode = Consoles.ProductCode').fetchone()
    # Grab recents
    recent_added = conn.execute('SELECT * FROM Products INNER JOIN Consoles ON Products.ProductCode = Consoles.ProductCode ORDER BY Products.ProductID DESC LIMIT 5').fetchall()
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
        conn.execute(f"DELETE FROM Products, Consoles WHERE ProductCode = '{code}'")
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
    result = conn.execute(f"SELECT * FROM Products LEFT JOIN Consoles ON Products.ProductCode = Consoles.ProductCode WHERE Consoles.ProductCode = '{code}'").fetchall()
    conn.close()
    return render_template('item.html', result=result)


@app.route('/addconsole/', methods=('GET', 'POST'))
def addconsole():
    if request.method == 'POST':
        name = request.form['nameoptions']
        model = request.form['model']
        board = request.form['board']
        mods = request.form['mods']

        if not name:
            flash('Name is required!')
        elif not model:
            flash('Model is required!')
        elif not board:
            flash('Board Revision is required!')
        else:
            # Create the Console
            system = Console(name, model, board, mods)
            # Create the QR Code
            create_QR(system)

            conn = get_db_connection()
            conn.execute('INSERT INTO Products (ProductName, AcquiredDate, ProductCode) VALUES (?, ?, ?)',
                         (system.name, system.date, system.product_code))
            conn.commit()
            conn.execute('INSERT INTO Consoles (ConsoleModel, ConsoleBoard, ConsoleMods, ProductCode) VALUES (?, ?, ?, ?)',
                         (system.model, system.board, system.mods, system.product_code))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('addconsole.html')


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

            if not name:
                flash('Name is required!')
            else:
                # Add the new console type and save the image
                conn = get_db_connection()
                conn.execute(f"INSERT INTO ConsoleTypes (TypeName, ImgFile) VALUES ('{name}', '{filename}')")
                conn.commit()
                conn.close()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash(f'Console {name} successfully added.')
            return redirect(request.url)

    return render_template('add_console_type.html')


def create_QR(item):
    '''Creates a QR Code for easy access.
    '''
    qrcode = segno.make(f'http://127.0.0.1:5000/item/{item.product_code}')
    qrcode.save(f'./static/qrcodes/{item.product_code}.png', light='lightblue', scale='10')
