from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# MySQL Database Configuration
def connect_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="worker_user_service",
        password="usingservices",
        database="finance_tracker",
        #auth_plugin="caching_sha2_password"
    )

# Function to get a database connection
#def get_db_connection():
#    return mysql.connector.connect(**db_config)

# Render Login Page
@app.route('/')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Render Register Page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# User Registration Route
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name", "")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    dob = data.get("dob")

    if not first_name or not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = connect_mysql()  # ✅ Use connect_mysql()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (first_name, last_name, username, email, password_hash, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, username, email, password_hash, dob))

        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 409
    finally:
        cursor.close()
        conn.close()


# User Login Route
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = connect_mysql()  # ✅ Use connect_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id FROM users WHERE username = %s AND password_hash = %s", 
                   (username, password_hash))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        response = jsonify({
            "message": "Login successful",
            "user_id": user["user_id"],
            "redirect": "/dashboard"
        })
        response.set_cookie("user_id", str(user["user_id"]), httponly=True)  # ✅ Store user_id in cookie
        return response, 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/delete-user', methods=["POST"])
def delete_user():
    data = request.json
    user_id = data.get("user_id")
    username = data.get("username")

    if not user_id or not username:
        return jsonify({"error": "User ID and Username are required"}), 400

    conn = connect_mysql()  # ✅ Use the correct function
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s AND username = %s", (user_id, username))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": f"User {username} deleted successfully"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

