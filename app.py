from flask import Flask, request, jsonify, redirect
import sqlite3
import string
import random

app = Flask(__name__)


# -----------------------------
# Database
# -----------------------------

def get_db():
    conn = sqlite3.connect("urls.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Generate Short Code
# -----------------------------

def generate_code(length=6):
    characters = string.ascii_letters + string.digits

    code = ''.join(
        random.choice(characters)
        for _ in range(length)
    )

    return code


# -----------------------------
# Check if Code Exists
# -----------------------------

def code_exists(short_code):

    conn = get_db()

    result = conn.execute(
        "SELECT * FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()

    if result:
        return True
    else:
        return False


# -----------------------------
# Create Short URL
# -----------------------------

@app.route("/shorten", methods=["POST"])
def shorten_url():

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({
            "error": "URL is required"
        }), 400

    original_url = data["url"]

    # URL validation
    if not original_url.startswith(("http://", "https://")):
        return jsonify({
            "error": "Invalid URL"
        }), 400

    # Generate unique short code
    short_code = generate_code()

    while code_exists(short_code):
        short_code = generate_code()

    conn = get_db()

    conn.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "original_url": original_url,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201


# -----------------------------
# Redirect
# -----------------------------

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):

    conn = get_db()

    result = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()

    if result is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    return redirect(result["original_url"])


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":
    create_table()
    app.run(debug=True)