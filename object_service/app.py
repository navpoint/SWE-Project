from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime

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

# Route to Get All Plans
@app.route('/plans', methods=['GET'])
def get_plans():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT plan_id, name, description FROM plans WHERE user_id = %s", (user_id,))
    plans = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify({"plans": plans})

# Route to Get All Goals
@app.route('/goals', methods=['GET'])
def get_goals():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT goal_id, name, description, target_amount, progress, is_current, last_update FROM goals WHERE user_id = %s", (user_id,))
    goals = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"goals": goals})


# Route to Create a Plan
@app.route('/create-plan', methods=['POST'])
def create_plan():
    data = request.json
    user_id = data.get("user_id")
    plan_name = data.get("name")
    description = data.get("description", "")

    if not user_id or not plan_name:
        return jsonify({"error": "User ID and Plan name are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO plans (user_id, name, description) VALUES (%s, %s, %s)", (user_id, plan_name, description))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Plan created successfully"}), 201

# Route to Create a Goal and Attach It to a Plan
@app.route('/create-goal', methods=['POST'])
def create_goal():
    data = request.json
    user_id = data.get("user_id")
    name = data.get("name")
    description = data.get("description", "")
    target_amount = data.get("target_amount", None)

    if not user_id or not name:
        return jsonify({"error": "User ID and Goal Name are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO goals (user_id, name, description, target_amount, progress, is_current, last_update)
            VALUES (%s, %s, %s, %s, 0, 'Y', NOW())
        """, (user_id, name, description, target_amount))

        conn.commit()
        return jsonify({"message": "Goal added successfully"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()



# Route to Create a Cash Flow Entry
@app.route('/create-cashflow', methods=['POST'])
def create_cashflow():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description", "")
    flow_type = data.get("flow_type")  # "income" or "expense"
    frequency = data.get("frequency")  # One Time, Daily, Weekly, etc.
    date = datetime.now().strftime('%Y-%m-%d')  # Default to current date

    if not user_id or not amount or not category or not flow_type or not frequency:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cash_flows (user_id, amount, category, description, flow_type, frequency, date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, amount, category, description, flow_type, frequency, date))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Cash Flow entry created successfully"}), 201

@app.route('/add-plan', methods=['POST'])
def add_plan():
    data = request.json
    user_id = data.get("user_id")
    plan_name = data.get("name")
    description = data.get("description", "")

    if not user_id or not plan_name:
        return jsonify({"error": "User ID and Plan Name are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO plans (user_id, name, description)
            VALUES (%s, %s, %s)
        """, (user_id, plan_name, description))

        conn.commit()
        return jsonify({"message": "Plan added successfully"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/user-plans', methods=['GET'])
def get_user_plans():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT plan_id, name FROM plans WHERE user_id = %s", (user_id,))
    plans = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"plans": plans})


if __name__ == '__main__':
    app.run(port=5002, debug=True)
