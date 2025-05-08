from flask import Flask, render_template, request, redirect, url_for, session, flash # type: ignore
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # ✅ Menu Table (includes image and description)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        image TEXT,
        calories INTEGER,
        protein REAL,
        fat REAL,
        carbs REAL
        )
    """)

    # ✅ Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # ✅ Optional Cart Table (if you want to store cart items in DB)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            description TEXT
        )
    """)

    # ✅ Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            image TEXT,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()

# 🔁 Initialize tables when the app starts
init_db()


@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Account created. Please log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists.")
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('landing_page'))

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu')
    items = cursor.fetchall()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        description = request.form['description']
        image = request.form['image']

        calories = request.form.get('calories') or 0
        protein = request.form.get('protein') or 0
        fat = request.form.get('fat') or 0
        carbs = request.form.get('carbs') or 0

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO menu (name, category, price, description, image, calories, protein, fat, carbs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, category, price, description, image, calories, protein, fat, carbs))

        conn.commit()
        conn.close()
        return redirect(url_for('menu'))
    return render_template('add_item.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/menu/<category>')
def menu_category(category):
    try:
        return render_template(f'menu/{category}.html')
    except:
        return f"<h1>{category.title()} Menu</h1><p>Page not found.</p>", 404

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        flash("Please login first to add items to cart!")
        return redirect(url_for('login'))

    item_name = request.form['item_name']
    price = float(request.form['price'])
    image = request.form.get('image','')
    description = request.form.get('description', '')

    cart = session.get('cart', [])
    for item in cart:
        if item['name'] == item_name:
            item['quantity'] += 1
            break
    else:
        cart.append({'name': item_name, 
                     'price': price,
                     'image': image,
                     'description': description, 
                     'quantity': 1})

    session['cart'] = cart
    flash(f"{item_name} added to cart!")
    return redirect(request.referrer or url_for('index'))

@app.route('/cart')
def cart():
    if 'username' not in session:
        flash('Please login to view your cart.')
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)



@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    name = request.form.get('name')
    action = request.form.get('action')
    cart = session.get('cart', [])

    for item in cart:
        if item['name'] == name:
            if action == 'increase':
                item['quantity'] += 1
            elif action == 'decrease':
                item['quantity'] = max(1, item['quantity'] - 1)
            elif action == 'remove':
                cart.remove(item)
            break

    if action == 'checkout':
        session.pop('cart', None)
        flash('Order placed successfully!')
        return redirect(url_for('index'))

    session['cart'] = cart
    return redirect(url_for('cart'))

from datetime import datetime

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'username' not in session:
        flash("Please login to place an order.")
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    if not cart:
        flash("Your cart is empty.")
        return redirect(url_for('cart'))

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    for item in cart:
        cursor.execute("""
            INSERT INTO orders (username, item_name, quantity, price, image, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session['username'],
            item['name'],
            item['quantity'],
            item['price'],
            item.get('image', ''),
            item.get('description', '')
        ))

    conn.commit()
    conn.close()

    # Clear cart after successful order
    session.pop('cart', None)
    flash("✅ Your order has been placed successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
