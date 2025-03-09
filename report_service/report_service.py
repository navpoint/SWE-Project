from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

# Function to connect to MySQL database
def connect_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="worker_user_service",
        password="usingservices",
        database="finance_tracker",
        autocommit=True  # ✅ Ensures changes are committed immediately
    )

@app.route('/get-report', methods=['POST'])
def get_report():
    data = request.json
    plan_id = data.get("plan_id")
    user_id = data.get("user_id")
    current_savings = data.get("current_savings", 0)

    if not plan_id or not user_id:
        return jsonify({"error": "Missing plan_id or user_id"}), 400

    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)

    # ✅ Retrieve cash flows for this plan
    cursor.execute("SELECT amount, category, flow_type, frequency FROM cash_flows WHERE plan_id = %s", (plan_id,))
    cash_flows = cursor.fetchall()
    conn.close()

    # ✅ Categorization
    incomes = []
    expenses = []
    income_monthly = 0
    expense_monthly = 0
    one_time_income = 0
    one_time_expense = 0
    annual_income = 0
    annual_expense = 0

    for flow in cash_flows:
        amount = float(flow["amount"])
        entry = {"amount": amount, "category": flow["category"], "frequency": flow["frequency"]}

        if flow["flow_type"] == "Income":
            incomes.append(entry)
            if flow["frequency"] == "Monthly":
                income_monthly += amount
            elif flow["frequency"] == "One Time":
                one_time_income += amount
            elif flow["frequency"] == "Annually":
                annual_income += amount
        else:
            expenses.append(entry)
            if flow["frequency"] == "Monthly":
                expense_monthly += amount
            elif flow["frequency"] == "One Time":
                one_time_expense += amount
            elif flow["frequency"] == "Annually":
                annual_expense += amount

    # ✅ Build Budget Report
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    year = 2025
    savings = current_savings
    report = []

    for i in range(12):
        projected_savings = savings + income_monthly - expense_monthly
        if i == 11:  # December: Apply one-time and annual cash flows
            projected_savings += one_time_income - one_time_expense + annual_income - annual_expense
        savings = projected_savings

        report.append({"month": f"{months[i]}, {year}", "projected_savings": projected_savings})

    return jsonify({
        "incomes": incomes,
        "expenses": expenses,
        "budget_report": report
    })

@app.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.json
    print("Received data:", data)  # Debugging log

    current_savings = data.get("current_savings", 0)
    cash_flows = data.get("cash_flows", [])

    # Categorized lists for UI
    categorized_cash_flows = {
        "income_monthly": [],
        "income_other": [],
        "income_onetime": [],
        "expense_monthly": [],
        "expense_other": [],
        "expense_onetime": []
    }

    # Summarized values for report calculations
    income_monthly = 0
    expense_monthly = 0
    one_time_income = 0
    one_time_expense = 0
    annual_income = 0
    annual_expense = 0

    # Categorizing cash flows
    for flow in cash_flows:
        amount = float(flow["amount"])
        entry = {"amount": amount, "category": flow["category"]}

        if flow["flow_type"] == "Income":
            if flow["frequency"] == "Monthly":
                categorized_cash_flows["income_monthly"].append(entry)
                income_monthly += amount
            elif flow["frequency"] == "One Time":
                categorized_cash_flows["income_onetime"].append(entry)
                one_time_income += amount
            else:
                categorized_cash_flows["income_other"].append(entry)
                if flow["frequency"] == "Annually":
                    annual_income += amount
        else:  # Expenses
            if flow["frequency"] == "Monthly":
                categorized_cash_flows["expense_monthly"].append(entry)
                expense_monthly += amount
            elif flow["frequency"] == "One Time":
                categorized_cash_flows["expense_onetime"].append(entry)
                one_time_expense += amount
            else:
                categorized_cash_flows["expense_other"].append(entry)
                if flow["frequency"] == "Annually":
                    annual_expense += amount

    # Generate 12-month budget report
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    year = 2025
    savings = current_savings
    report = []

    for i in range(12):
        projected_savings = savings + income_monthly - expense_monthly
        if i == 11:  # December: Apply annual & one-time incomes/expenses
            projected_savings += one_time_income - one_time_expense + annual_income - annual_expense
        savings = projected_savings

        report.append({
            "month": f"{months[i]}, {year}",
            "projected_savings": projected_savings
        })

    return jsonify({
        "categorized_cash_flows": categorized_cash_flows,
        "report": report
    })

@app.route('/estimate-long-term', methods=['POST'])
def estimate_long_term():
    data = request.json
    print("📩 Received long-term estimate request:", data)  # Debugging log

    plan_id = data.get("plan_id")
    user_id = data.get("user_id")
    selected_month = data.get("selected_month", 1)  # Default: January
    selected_year = data.get("selected_year", 2025)  # Default: Current Year
    current_savings = data.get("current_savings", 0)

    # ✅ Log received data for debugging
    print(f"🔹 plan_id: {plan_id}, user_id: {user_id}, selected_month: {selected_month}, selected_year: {selected_year}, current_savings: {current_savings}")

    if not plan_id or not user_id:
        print("❌ Missing plan_id or user_id!")
        return jsonify({"error": "Missing plan_id or user_id"}), 400

    # ✅ Fetch cash flows for the plan
    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT amount, flow_type, frequency FROM cash_flows WHERE plan_id = %s", (plan_id,))
    cash_flows = cursor.fetchall()

    conn.close()

    # ✅ Initialize cash flow categories
    income_monthly = 0
    expense_monthly = 0
    one_time_income = 0
    one_time_expense = 0
    annual_income = 0
    annual_expense = 0

    for flow in cash_flows:
        amount = flow["amount"]
        flow_type = flow["flow_type"]
        frequency = flow["frequency"]

        if flow_type == "Income":
            if frequency == "Monthly":
                income_monthly += amount
            elif frequency == "One Time":
                one_time_income += amount
            elif frequency == "Annually":
                annual_income += amount
        else:  # Expense
            if frequency == "Monthly":
                expense_monthly += amount
            elif frequency == "One Time":
                one_time_expense += amount
            elif frequency == "Annually":
                annual_expense += amount

    # ✅ Determine months to project
    from datetime import datetime
    current_year = datetime.now().year
    current_month = datetime.now().month
    months_to_project = (selected_year - current_year) * 12 + (selected_month - current_month)

    savings = current_savings

    # ✅ Project savings month by month
    for i in range(months_to_project):
        savings += income_monthly - expense_monthly
        if (i + current_month) % 12 == 0:  
            savings += annual_income - annual_expense

    print(f"✅ Estimated Savings: {savings}")  # Debugging log

    response = {"projected_savings": float(savings)}  # ✅ Ensure it's always a float
    print("📤 Sending response:", response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5004, debug=True)
