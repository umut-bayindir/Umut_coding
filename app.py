import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management and flash messages

# Database configuration
DATABASE_CONFIG = {
    "dbname": "A4_db",
    "user": "admin",
    "password": "1Admin&Elliot",  # In production, use environment variables or config files
    "host": "localhost",
    "port": "5432",
}

# Function to establish a database connection
def get_db_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

# Function to create tables
def create_tables():
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL for creating tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Roles (
            id SERIAL PRIMARY KEY,
            role_name VARCHAR(50) UNIQUE NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Department(
            dnumber INT PRIMARY KEY,
            dname VARCHAR(50) UNIQUE NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role_id INT REFERENCES Roles(id),
            department_id INT REFERENCES Department(dnumber)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project(
            pid SERIAL PRIMARY KEY,
            dnum INT REFERENCES Department(dnumber)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee(
            eid SERIAL PRIMARY KEY,
            dno INT REFERENCES Department(dnumber),
            pid INT REFERENCES Project(pid)
        );
        """)

        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")
    finally:
        if connection:
            connection.close()


def populate_tables(): 
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL for creating tables
        cursor.execute(
            "INSERT INTO Roles (role_name) VALUES (%s)", ("admin",))
        cursor.execute(
            "INSERT INTO Roles (role_name) VALUES (%s)", ("department_head",))
        cursor.execute(
            "INSERT INTO Roles (role_name) VALUES (%s)", ("employee",))

        cursor.execute(
            "INSERT INTO Department (dnumber,dname) VALUES (%s,%s)", (1,"Computing",))

        cursor.execute(
            "INSERT INTO Department (dnumber,dname) VALUES (%s,%s)", (2,"Plumbing",))

    
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"An error occurred while populating tables: {e}")
    finally:
        if connection:
            connection.close()


# Route for home page
@app.route("/")
def home():
    username = None
    user_id = session.get('user_id')
    if user_id:
        # Fetch the username from the database using the user_id
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT username FROM Users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                username = result[0]
            cursor.close()
        except Exception as e:
            print(f"An error occurred while fetching the username: {e}")
        finally:
            if connection:
                connection.close()
    return render_template("index.html", username=username)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate form data
        if not username or not password:
            flash("Please enter both username and password.")
            return redirect(url_for("login"))

        # Check credentials
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query the database for the user
            cursor.execute("""
            SELECT id, password_hash FROM Users WHERE username = %s
            """, (username,))
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user[1], password):
                # Credentials are valid
                session['user_id'] = user[0]
                flash("Login successful!")
                return redirect(url_for("home"))
            else:
                flash("Invalid username or password.")
                return redirect(url_for("login"))

        except Exception as e:
            print(f"An error occurred during login: {e}")
            flash("An error occurred. Please try again.")
            return redirect(url_for("login"))
        finally:
            if connection:
                connection.close()
    else:
        # Render login template
        return render_template("login.html")

# Logout feature
@app.route('/logout')
def logout():
    # Remove 'user_id' from the session to log out the user
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        dno = request.form['department_id']
        role = request.form['role_id']

        # Validate form data
        if not username or not password or not dno or not role:
            flash("Please fill out all fields.")
            return redirect(url_for("register"))

        # Hash the password
        password_hash = generate_password_hash(password)

        # Insert new user into the database
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert user into Users table
            cursor.execute("""
            INSERT INTO Users (username, password_hash, role_id, department_id)
            VALUES (%s, %s, %s, %s)
            """, (username, password_hash, role, dno))

            connection.commit()
            cursor.close()

            flash("Registration successful!")
            return redirect(url_for("home"))

        except psycopg2.IntegrityError:
            # Handle duplicate username
            connection.rollback()
            flash("Username already exists.")
            return redirect(url_for("register"))
        except Exception as e:
            print(f"An error occurred during registration: {e}")
            flash("An error occurred. Please try again.")
            return redirect(url_for("register"))
        finally:
            if connection:
                connection.close()
    else:
        # Render registration template
        return render_template("register.html")

# (Optional) Show user route
@app.route('/show_user')
def show_user():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view this page.')
        return redirect(url_for('login'))
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id,username,role_id FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return render_template('show_user.html', user=user)
        else:
            flash('User not found.')
            return redirect(url_for('home'))
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred. Please try again.')
        return redirect(url_for('home'))
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    create_tables()  # Ensure the tables are created
    # populate_tables() 
    app.run(debug=True)
