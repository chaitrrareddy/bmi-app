# DevOps Casestudy/app.py
from flask import Flask, render_template, request, g
import sqlite3
import os
from datetime import datetime

# Location of sqlite DB inside container; override with env var if needed
DB_PATH = os.environ.get("SQLITE_DB", "/data/bmi_history.db")

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        db = g._database = sqlite3.connect(DB_PATH, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS bmi_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT,
        created_at TEXT
    )""")
    db.commit()

@app.before_request
def startup():
    init_db()

@app.teardown_appcontext
def close_connection(exc):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            weight = float(request.form.get("weight", 0))
            height_cm = float(request.form.get("height_cm", 0))
            if height_cm <= 0 or weight <= 0:
                raise ValueError("Weight and height must be positive numbers.")
            height_m = height_cm / 100.0
            bmi = round(weight / (height_m * height_m), 2)
            category = bmi_category(bmi)

            db = get_db()
            db.execute(
                "INSERT INTO bmi_history (weight, height, bmi, category, created_at) VALUES (?, ?, ?, ?, ?)",
                (weight, height_cm, bmi, category, datetime.utcnow().isoformat())
            )
            db.commit()

            result = {"weight": weight, "height": height_cm, "bmi": bmi, "category": category}
        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)

@app.route("/history")
def history():
    db = get_db()
    cur = db.execute("SELECT * FROM bmi_history ORDER BY created_at DESC LIMIT 100")
    rows = cur.fetchall()
    return render_template("history.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
