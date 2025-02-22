from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/create-plan')
def create_plan_page():
    return render_template("create_plan.html")

@app.route('/create-goal')
def create_goal_page():
    return render_template("create_goal.html")

@app.route('/help')
def help_page():
    return render_template("help.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")  # This will render the FAQ page

@app.route('/logout')
def logout():
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
