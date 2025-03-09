from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, session
import zmq
import json
import os
import time
import pymysql

app = Flask(__name__)
app.secret_key = "myhardcodedsecretkey123"  # ✅ Hardcoded key for session management

def connect_mysql():
    return pymysql.connect(
        host="localhost",
        user="worker_user_service",
        password="usingservices",
        database="finance_tracker",
        cursorclass=pymysql.cursors.DictCursor  #  # Ensures dictionary-style results
    )

# ZeroMQ Setup to communicate with receiver.py
context = zmq.Context()
client_socket = context.socket(zmq.REQ)
client_socket.connect("tcp://localhost:33333")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    database = connect_mysql()
    cursor = database.cursor()
    user_id = request.args.get("user_id") 
    
    # Fetch all plans for the logged-in user
    user_id = request.cookies.get("user_id")  # Ensure user ID is being stored in cookies
    cursor.execute("SELECT * FROM plans WHERE user_id = %s", (user_id,))
    plans = cursor.fetchall()

    database.close()

    return render_template("dashboard.html", plans=plans)



@app.route('/create-plan')
def create_plan():
    user_id = request.args.get("user_id")
    if not user_id:
        return redirect(url_for('login'))  # Prevent access if no user ID
    return render_template('create_plan.html', user_id=user_id)

@app.route('/create-goal')
def create_goal():
    user_id = request.args.get("user_id")
    if not user_id:
        return redirect(url_for('login'))
    return render_template('create_goal.html', user_id=user_id)


@app.route('/help')
def help_page():
    return render_template("help.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

@app.route("/export-data", methods=["POST"])
def export_data():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"success": False, "error": "Missing user ID"})

    # Send request to receiver.py via ZeroMQ
    request_json = json.dumps({"user_id": user_id})
    client_socket.send_string(request_json)

    # Receive response
    response = client_socket.recv().decode()

    if "File successfully received!" in response:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": response})

@app.route("/download-csv")
def download_csv():
    file_path = "export/user_data_export.csv"

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"success": False, "error": "File not found. Try exporting again."})

@app.route("/plan/<int:plan_id>")
def view_plan(plan_id):
    database = connect_mysql()
    cursor = database.cursor()  

    cursor.execute("SELECT * FROM plans WHERE plan_id = %s", (plan_id,))
    plan = cursor.fetchone()

    if not plan:
        return "Plan not found", 404

    cursor.execute("SELECT * FROM cash_flows WHERE plan_id = %s", (plan_id,))
    cash_flows = cursor.fetchall()

    # ✅ Fetch user info from the database
    user_id = request.args.get("user_id")
    cursor.execute("SELECT username, first_name FROM users WHERE user_id = %s", (user_id,))
    user_info = cursor.fetchone()

    database.close()

    return render_template(
        "plan.html",
        plan=plan,
        cash_flows=cash_flows,
        user_id=user_id,
        username=user_info["username"] if user_info else None,
        first_name=user_info["first_name"] if user_info else None
    )

@app.route("/goal/<int:goal_id>")
def view_goal(goal_id):
    database = connect_mysql()
    cursor = database.cursor()

    # ✅ Fetch goal details
    cursor.execute("SELECT * FROM goals WHERE goal_id = %s", (goal_id,))
    goal = cursor.fetchone()

    if not goal:
        return "Goal not found", 404

    # ✅ Fetch associated events & habits
    cursor.execute("SELECT * FROM events WHERE goal_id = %s", (goal_id,))
    events = cursor.fetchall()

    cursor.execute("SELECT * FROM habits WHERE goal_id = %s", (goal_id,))
    habits = cursor.fetchall()

    # ✅ Fetch user info from the database
    user_id = request.args.get("user_id")
    cursor.execute("SELECT username, first_name FROM users WHERE user_id = %s", (user_id,))
    user_info = cursor.fetchone()

    database.close()

    return render_template(
        "goal.html",
        goal=goal,
        events=events,
        habits=habits,
        user_id=user_id,
        username=user_info["username"] if user_info else None,
        first_name=user_info["first_name"] if user_info else None
    )


@app.route("/add-cash-flow/<int:plan_id>", methods=["GET", "POST"])
def add_cash_flow(plan_id):
    # ✅ Retrieve user_id from query string
    user_id = request.args.get("user_id")

    if request.method == "POST":
        user_id = request.form.get("user_id")  # Ensure it's included in form submission
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        flow_type = request.form.get("flow_type")
        frequency = request.form.get("frequency")
        date = request.form.get("date")

        database = connect_mysql()
        cursor = database.cursor()

        try:
            cursor.execute("""
                INSERT INTO cash_flows (user_id, plan_id, amount, category, description, flow_type, frequency, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, plan_id, amount, category, description, flow_type, frequency, date))

            database.commit()
            return redirect(url_for("view_plan", plan_id=plan_id, user_id=user_id))
        except pymysql.err.IntegrityError as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            database.close()

    return render_template("add_cash_flow.html", plan_id=plan_id, user_id=user_id)

@app.route("/add-event/<int:goal_id>", methods=["GET", "POST"])
def add_event(goal_id):
    user_id = request.args.get("user_id")

    if request.method == "POST":
        user_id = request.form.get("user_id")
        description = request.form.get("description")

        # ✅ Use Flask’s `request` module to send data to object_service.py
        import urllib.request
        import json

        api_url = "http://127.0.0.1:5002/store-event"
        event_data = json.dumps({
            "user_id": user_id,
            "goal_id": goal_id,
            "description": description
        }).encode("utf-8")

        req = urllib.request.Request(api_url, data=event_data, headers={'Content-Type': 'application/json'}, method='POST')

        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.load(response)
                if response_data.get("success"):
                    return redirect(url_for("view_goal", goal_id=goal_id, user_id=user_id))
                else:
                    return f"Error storing event: {response_data.get('error')}", 500
        except urllib.error.URLError as e:
            return f"Error communicating with object_service: {str(e)}", 500

    return render_template("add_event.html", goal_id=goal_id, user_id=user_id)


@app.route("/add-habit/<int:goal_id>", methods=["GET", "POST"])
def add_habit(goal_id):
    user_id = request.args.get("user_id")

    if request.method == "POST":
        user_id = request.form.get("user_id")
        name = request.form.get("name")
        description = request.form.get("description")

        # ✅ Use Flask’s `request` module to send data to object_service.py
        import urllib.request
        import json

        api_url = "http://127.0.0.1:5002/store-habit"
        habit_data = json.dumps({
            "user_id": user_id,
            "goal_id": goal_id,
            "name": name,
            "description": description
        }).encode("utf-8")

        req = urllib.request.Request(api_url, data=habit_data, headers={'Content-Type': 'application/json'}, method='POST')

        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.load(response)
                if response_data.get("success"):
                    return redirect(url_for("view_goal", goal_id=goal_id, user_id=user_id))
                else:
                    return f"Error storing habit: {response_data.get('error')}", 500
        except urllib.error.URLError as e:
            return f"Error communicating with object_service: {str(e)}", 500

    return render_template("add_habit.html", goal_id=goal_id, user_id=user_id)

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
