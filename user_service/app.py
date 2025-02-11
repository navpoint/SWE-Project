from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "worker_user_service",
    "password": "usingservices",
    "database": "finance_tracker"
}

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

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

    conn = get_db_connection()
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

# User Login Route (No Sessions)
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id FROM users WHERE username = %s AND password_hash = %s", 
                   (username, password_hash))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user["user_id"],  # ✅ Ensure user_id is sent back
            "redirect": "/dashboard"
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401


# ✅ New Route: Get User ID by Username
@app.route('/get-user-id', methods=['GET'])
def get_user_id():
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"user_id": user["user_id"]})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
