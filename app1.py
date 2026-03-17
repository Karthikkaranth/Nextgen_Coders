from flask import Flask, request, jsonify, render_template, redirect, session
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Secret key from .env
app.secret_key = os.getenv("SECRET_KEY")

# ======================
# 🔐 MONGODB CONNECTION (SECURE)
# ======================

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["userDB"]
users = db["users"]

# ======================
# 🔹 PAGE ROUTES
# ======================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/chat")
def chat():
    if "user" in session:
        return render_template("chat.html", username=session["user"])
    return redirect("/")

# ======================
# 🔹 REGISTER
# ======================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"status": "error", "msg": "Missing fields"})

    existing_user = users.find_one({
        "$or": [
            {"email": email},
            {"username": username}
        ]
    })

    if existing_user:
        return jsonify({"status": "user_exists"})

    users.insert_one({
        "username": username,
        "email": email,
        "password": password
    })

    return jsonify({"status": "success"})

# ======================
# 🔹 LOGIN
# ======================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    user = users.find_one({
        "username": username,
        "password": password
    })

    if user:
        session["user"] = username
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

# ======================
# 🔹 LOGOUT
# ======================

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ======================
if __name__ == "__main__":
    app.run(debug=True)