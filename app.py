from flask import Flask, render_template, redirect, request, session, url_for, flash
import sqlite3
import bcrypt
import jwt
import datetime

app = Flask(__name__)
app.secret_key = "securekey123"

JWT_SECRET = "jwtsecretkey123"


# -------------------------
# Database Initialization
# -------------------------
def init_db():
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


# -------------------------
# Register
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed)
            )
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash("Username or Email already exists!", "danger")

        conn.close()

    return render_template('register.html')


# -------------------------
# Login + JWT
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user[3]

            if bcrypt.checkpw(password.encode(), stored_password):
                token = jwt.encode({
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, JWT_SECRET, algorithm="HS256")

                session['jwt'] = token
                return redirect(url_for('dashboard'))

        flash("Invalid username or password!", "danger")

    return render_template('login.html')


# -------------------------
# Dashboard (Protected)
# -------------------------
@app.route('/dashboard')
def dashboard():
    token = session.get('jwt')

    if not token:
        flash("Unauthorized! Please login first.", "danger")
        return redirect(url_for('login'))

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username = decoded["username"]

        # Get IP Address
        user_ip = request.remote_addr

        # Create readable session ID
        session_id = token[:15]

        return render_template(
            'dashboard.html',
            username=username,
            ip=user_ip,
            session_id=session_id
        )

    except:
        flash("Session expired! Login again.", "danger")
        return redirect(url_for('login'))



# -------------------------
# Homepage
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')


# -------------------------
# Logout
# -------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))


# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
