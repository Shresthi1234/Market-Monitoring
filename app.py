from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "farmer_market_db"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/<role>", methods=["POST"])
def login(role):
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if role not in ("farmer", "admin"):
        return redirect(url_for("home"))

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    table = "farmers" if role == "farmer" else "admins"
    cur.execute(f"SELECT id, username FROM {table} WHERE username=%s AND password=%s",
                (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        flash("Invalid username or password.")
        return redirect(url_for("home"))

    session["role"] = role
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("farmer_dashboard" if role == "farmer" else "admin_dashboard"))

@app.route("/farmer")
def farmer_dashboard():
    if session.get("role") != "farmer":
        return redirect(url_for("home"))
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DISTINCT crop FROM market_prices ORDER BY crop")
    crops = [r["crop"] for r in cur.fetchall()]
    cur.execute("SELECT DISTINCT location FROM market_prices ORDER BY location")
    locations = [r["location"] for r in cur.fetchall()]
    cur.close(); conn.close()
    return render_template("farmer.html", crops=crops, locations=locations)

@app.route("/farmer/compare", methods=["POST"])
def farmer_compare():
    if session.get("role") != "farmer":
        return redirect(url_for("home"))

    crop = request.form["crop"]
    location = request.form["location"]
    farmer_price = float(request.form["farmer_price"])

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT market_name, price FROM market_prices
                   WHERE crop=%s AND location=%s ORDER BY price DESC""",
                (crop, location))
    markets = cur.fetchall()

    cur.execute("""INSERT INTO farmer_prices (farmer_id, crop, location, price)
                   VALUES (%s,%s,%s,%s)
                   ON DUPLICATE KEY UPDATE price=VALUES(price), updated_at=CURRENT_TIMESTAMP""",
                (session["user_id"], crop, location, farmer_price))
    conn.commit()
    cur.close(); conn.close()

    highest = max([m["price"] for m in markets], default=farmer_price)
    lowest = min([m["price"] for m in markets], default=farmer_price)
    return render_template("farmer.html", crops=get_options("crop"),
                           locations=get_options("location"), markets=markets,
                           crop=crop, location=location, farmer_price=farmer_price,
                           highest=highest, lowest=lowest)

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("home"))
    return render_template("admin.html", crops=get_options("crop"), locations=get_options("location"))

@app.route("/admin/prices", methods=["POST"])
def admin_prices():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    crop = request.form["crop"]
    location = request.form["location"]
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT id, market_name, price FROM market_prices
                   WHERE crop=%s AND location=%s ORDER BY market_name""",
                (crop, location))
    markets = cur.fetchall()
    cur.close(); conn.close()
    return render_template("admin.html", crops=get_options("crop"),
                           locations=get_options("location"), markets=markets,
                           crop=crop, location=location)

@app.route("/admin/update", methods=["POST"])
def admin_update():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    price_id = request.form["price_id"]
    price = float(request.form["price"])
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE market_prices SET price=%s, updated_at=CURRENT_TIMESTAMP WHERE id=%s",
                (price, price_id))
    conn.commit()
    cur.close(); conn.close()
    return redirect(url_for("admin_dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

def get_options(column):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT {column} FROM market_prices ORDER BY {column}")
    values = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    return values

if __name__ == "__main__":
    app.run(debug=True)
