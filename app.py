from flask import Flask, request, jsonify, redirect, render_template
import database
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
from urllib.parse import urlparse

from database import get_db, create_table, get_url, code_exists
from utils import generate_code

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)


# =========================================================
# CREATE SHORT URL
# =========================================================

@app.route("/shorten", methods=["POST"])
@limiter.limit("10 per minute")
def shorten():

    data = request.get_json(silent=True)

    print("DATA RECEIVED:", data)

    # Check JSON
    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    # Check URL
    if "url" not in data:
        return jsonify({
            "error": "URL is required"
        }), 400

    original_url = data["url"]

    # Check URL type
    if not isinstance(original_url, str):
        return jsonify({
            "error": "URL must be a string"
        }), 400

    # =====================================================
    # URL VALIDATION
    # =====================================================

    parsed_url = urlparse(original_url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        return jsonify({
            "error": "Invalid URL. Please provide a valid http:// or https:// URL"
        }), 400

    # =====================================================
    # CUSTOM CODE
    # =====================================================

    custom_code = data.get("custom_code")

    if custom_code:

        if not isinstance(custom_code, str):
            return jsonify({
                "error": "Custom code must be a string"
            }), 400

        if not custom_code.isalnum():
            return jsonify({
                "error": "Custom code must contain only letters and numbers"
            }), 400

        if code_exists(custom_code):
            return jsonify({
                "error": "Custom code already exists"
            }), 409

        short_code = custom_code

    else:

        # Generate unique code
        short_code = generate_code()

        while code_exists(short_code):
            short_code = generate_code()

    # =====================================================
    # EXPIRATION
    # =====================================================

    expires_at = None

    expires_in = data.get("expires_in")

    if expires_in is not None:

        try:
            expires_in = int(expires_in)

            if expires_in <= 0:
                return jsonify({
                    "error": "expires_in must be greater than 0"
                }), 400

            expires_at = (
                datetime.now() +
                timedelta(seconds=expires_in)
            ).isoformat()

        except (ValueError, TypeError):
            return jsonify({
                "error": "expires_in must be a number"
            }), 400

    # =====================================================
    # CREATED TIME
    # =====================================================

    created_at = datetime.now().isoformat()

    # =====================================================
    # SAVE TO DATABASE
    # =====================================================

    conn = get_db()

    conn.execute("""
        INSERT INTO urls
        (original_url, short_code, clicks, created_at, expires_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        original_url,
        short_code,
        0,
        created_at,
        expires_at
    ))

    conn.commit()
    conn.close()

    # =====================================================
    # RESPONSE
    # =====================================================

    return jsonify({
        "message": "Short URL created successfully",
        "original_url": original_url,
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}",
        "created_at": created_at,
        "expires_at": expires_at
    }), 201


# =========================================================
# URL INFORMATION
# =========================================================

@app.route("/info/<short_code>", methods=["GET"])
@limiter.limit("30 per minute")
def get_info(short_code):

    result = get_url(short_code)

    if result is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    return jsonify({
    "short_code": result["short_code"],
    "original_url": result["original_url"],
    "clicks": result["clicks"],
    "created_at": result["created_at"],
    "expires_at": result["expires_at"],
    "last_clicked_at": result["last_clicked_at"]
}), 200

# =========================================================
# CLICK ANALYTICS
# =========================================================

@app.route("/analytics/<short_code>", methods=["GET"])
@limiter.limit("30 per minute")
def get_analytics(short_code):

    result = get_url(short_code)

    if result is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    return jsonify({
        "short_code": result["short_code"],
        "original_url": result["original_url"],
        "total_clicks": result["clicks"],
        "created_at": result["created_at"],
        "last_clicked_at": result["last_clicked_at"]
    }), 200

# =========================================================
# CLICK HISTORY
# =========================================================

@app.route("/analytics/<short_code>/history", methods=["GET"])
@limiter.limit("30 per minute")
def get_click_history(short_code):

    # Check if short URL exists
    result = get_url(short_code)

    if result is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    conn = get_db()

    clicks = conn.execute(
        """
        SELECT clicked_at
        FROM clicks
        WHERE short_code = ?
        ORDER BY id DESC
        """,
        (short_code,)
    ).fetchall()

    conn.close()

    history = []

    for click in clicks:
        history.append({
            "clicked_at": click["clicked_at"]
        })

    return jsonify({
        "short_code": short_code,
        "total_clicks": len(history),
        "click_history": history
    }), 200

# =========================================================
# REDIRECT
# =========================================================

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):

    conn = get_db()

    result = conn.execute(
        "SELECT * FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    # Short code not found
    if result is None:

        conn.close()

        return jsonify({
            "error": "Short URL not found"
        }), 404

    # =====================================================
    # CHECK EXPIRATION
    # =====================================================

    if result["expires_at"]:

        expires_at = datetime.fromisoformat(
            result["expires_at"]
        )

        if datetime.now() >= expires_at:

            conn.close()

            return jsonify({
                "error": "Short URL has expired"
            }), 410

    # =====================================================
    # INCREASE CLICK COUNT
    # =====================================================
    last_clicked_at = datetime.now().isoformat()

    conn.execute(
        """
        UPDATE urls
        SET clicks = clicks + 1,
            last_clicked_at = ?
        WHERE short_code = ?
        """,
        (last_clicked_at, short_code)
    )
    conn.execute(
        """
        INSERT INTO clicks (short_code, clicked_at)
        VALUES (?, ?)
        """,
        (short_code, last_clicked_at)
    )

    conn.commit()
    conn.close()

    # Redirect to original URL
    return redirect(result["original_url"])


# =========================================================
# DELETE SHORT URL
# =========================================================

@app.route("/delete/<short_code>", methods=["DELETE"])
@limiter.limit("10 per minute")
def delete_url(short_code):

    result = get_url(short_code)

    if result is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    conn = get_db()

    conn.execute(
        "DELETE FROM urls WHERE short_code = ?",
        (short_code,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Short URL deleted successfully",
        "short_code": short_code
    }), 200
    
# =========================================================
# GET ALL SHORT URLs
# =========================================================

@app.route("/urls", methods=["GET"])
@limiter.limit("20 per minute")
def get_all_urls():

    conn = get_db()

    results = conn.execute(
        "SELECT * FROM urls ORDER BY id DESC"
    ).fetchall()

    conn.close()

    urls = []

    for result in results:

        urls.append({
            "short_code": result["short_code"],
            "original_url": result["original_url"],
            "clicks": result["clicks"],
            "created_at": result["created_at"],
            "expires_at": result["expires_at"]
        })

    return jsonify({
        "count": len(urls),
        "urls": urls
    }), 200

# =========================================================
# HOME
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return render_template("index.html")

# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_table()
database.add_analytics_column()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)