import sqlite3

DATABASE = "urls.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TEXT,
            expires_at TEXT,
            last_clicked_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT NOT NULL,
            clicked_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_analytics_column():
    conn = get_db()

    columns = conn.execute("PRAGMA table_info(urls)").fetchall()

    column_names = [column["name"] for column in columns]

    if "last_clicked_at" not in column_names:
        conn.execute(
            "ALTER TABLE urls ADD COLUMN last_clicked_at TEXT"
        )
        conn.commit()

    conn.close()


def get_url(short_code):
    conn = get_db()

    result = conn.execute(
        "SELECT * FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()

    return result


def code_exists(short_code):
    conn = get_db()

    result = conn.execute(
        "SELECT id FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()

    return result is not None