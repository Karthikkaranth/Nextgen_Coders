from flask import Flask, request, jsonify, render_template, redirect, session
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# 🔐 Secret key for session
app.secret_key = "supersecretkey"

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
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
    else:
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

    # 🔍 CHECK EXISTING USER (username OR email)
    existing_user = users.find_one({
        "$or": [
            {"email": email},
            {"username": username}
        ]
    })

    if existing_user:
        return jsonify({"status": "user_exists"})

    # ✅ SAVE USER
    users.insert_one({
        "username": username,
        "email": email,
        "password": password
    })

    return jsonify({"status": "success"})


# ======================
# 🔹 LOGIN (USERNAME BASED)
# ======================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    # 🔍 CHECK USERNAME + PASSWORD
    user = users.find_one({
        "username": username,
        "password": password
    })

    if user:
        session["user"] = username   # ✅ store session
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})


# ======================
# 🔹 LOGOUT (optional but useful)
# ======================

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ======================
if __name__ == "__main__":
    app.run(debug=True)