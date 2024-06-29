import qrcode
from flask import Flask, render_template, request, url_for, flash, redirect
from console import Console
from markupsafe import escape
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '1d5db266e7902199cc6cb39e6511cd81ccd9da827fa9deaf'
messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM Products INNER JOIN Consoles WHERE Products.ProductCode = Consoles.ProductCode').fetchall()
    conn.close()
    return render_template('index.html', results=results)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['nameoptions']
        model = request.form['model']
        board = request.form['board']

        if not name:
            flash('Name is required!')
        elif not model:
            flash('Model is required!')
        else:
            # Create the Console
            system = Console(name, model, board, [])
            # Create the QR Code
            create_QR(system)

            conn = get_db_connection()
            conn.execute('INSERT INTO Products (ProductName, AcquiredDate, ProductCode) VALUES (?, ?, ?)',
                         (system.name, system.date, system.product_code))
            conn.commit()
            conn.execute('INSERT INTO Consoles (ConsoleModel, ConsoleBoard, ProductCode) VALUES (?, ?, ?)',
                         (system.model, system.board, system.product_code))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route("/qr-code")
def create_QR(system):
    '''Creates a QR Code for easy access.
    '''
    img = qrcode.make(f'http://127.0.0.1:5000/item/{system.product_code}')
    type(img)
    img.save(f"./qrcodes/{system.product_code}.png")
