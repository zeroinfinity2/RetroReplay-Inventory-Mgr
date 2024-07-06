import segno
from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
import os
from werkzeug.utils import secure_filename
import datetime
from models import db, Product, Console, Goods, ConsoleType
from sqlalchemy import func


# Initialization --------------------------------------
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/inventory.db"
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()
# ------------------------------------------------------


def create_product_code(product_code, product_type, indate):
    """Creates product codes based on the unique info.
    """
    return f"{product_code}{product_type}{indate}"


def create_QR(product_code):
    '''Creates a QR Code for easy access.
    '''
    qrcode = segno.make(f'{product_code}')
    qrcode.save(f'./static/qrcodes/{product_code}.png', light='lightblue', scale='10')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    # Grab the console counts
    console_count = db.session.execute(db.select(func.count()).select_from(Product).join(Console, Product.product_code == Console.product_code)).scalar_one()
    # Grab recents added items
    recent_added = db.session.execute(db.select(Product).order_by(Product.product_code).limit(10)).scalars()
    return render_template('index.html', consoles=console_count, recent=recent_added)


@app.route('/item/<itemcode>', methods=('GET', 'POST'))
def item(itemcode):
    code = f'{escape(itemcode)}'

    # If the item sold returns the proper value (1)
    if request.form.get("itemsold"):
        # Get the sale status.
        sale_status = bool(request.form['itemsold'])

        # Select the item and update it's sales status, and commit to the database.
        updated_product = db.session.execute(db.select(Product).where(Product.product_code == f"{code}")).scalar_one()
        updated_product.is_sold = sale_status
        db.session.commit()
        flash("Item marked as sold.")

    # If modifications were made to mods
    if request.form.get("mods"):
        # Get the mods changes
        mods = request.form['mods']

        # Grab the product and update it's mods, and commit to the database.
        updated_product = db.session.execute(db.select(Console).where(Console.product_code == f"{code}")).scalar_one()
        updated_product.mods = mods
        db.session.commit()
        flash("Item updated successfully.")

    # If request to delete item was made
    if request.form.get("delete"):
        # Delete from the database
        product = db.session.execute(db.select(Product).where(Product.product_code == f"{code}")).scalar_one()
        console = db.session.execute(db.select(Console).where(Console.product_code == f"{code}")).scalar_one()

        db.session.delete(console)
        db.session.delete(product)
        db.session.commit()

        # Delete the QR code file
        if os.path.exists(f"static/qrcodes/{code}.png"):
            os.remove(f"static/qrcodes/{code}.png")
        # Go back to index after delete
        flash("Item successfully removed from the database.")
        return redirect(url_for('index'))

    # Show the item

    # Find the result if it exists.
    result = db.session.execute(db.select(Product, Console).join(Console, Product.product_code == Console.product_code).where(Console.product_code == f"{code}"))
    return render_template('item.html', result=result)


@app.route('/addconsole/', methods=('GET', 'POST'))
def addconsole():
    # Grab all of the console codes
    consoles = db.session.execute(db.select(ConsoleType)).scalars()

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
            # If a console is being added, find the console's fullname
            for console in consoles:
                if console.code_name == console_code:
                    console_name = console.full_name

            # Generate the in-date
            sys_indate = datetime.datetime.now().strftime("%m%d%Y%H%M%S")

            # Generate Product Code
            product_code = create_product_code(console_code, product_type, sys_indate)

            # Create the QR Code
            create_QR(product_code)

            # Create the product
            new_product = Product(
                name=console_name,
                code_name=console_code,
                in_date=sys_indate,
                type_of=product_type,
                is_sold=0,
                cost=float(cost),
                price=float(0.0),
                product_code=product_code
            )

            # Create the Console
            new_console = Console(
                mods=console_mods,
                model=console_model,
                board=console_board,
                product_code=product_code,
                code_name=console_code
            )

            # Add the new product and commit.
            db.session.add(new_product)
            db.session.add(new_console)
            db.session.commit()
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
            console_name = request.form['console_name']
            console_code = request.form['console_code']

            if not console_name:
                flash('Name is required!')
            else:
                # Rename the filename to the codename of the console "CODE.PNG"
                filename = f"{console_code}.{filename.rsplit('.')[1].lower()}"

                # Add the new console type and save the image
                new_console_type = ConsoleType(
                    code_name=console_code,
                    full_name=console_name,
                    img_src=filename
                )

                db.session.add(new_console_type)
                db.session.commit()

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash(f'Console {console_name} successfully added.')
            return redirect(request.url)

    return render_template('add_console_type.html')
