import sqlite3

DATABASE = "urls.db"


def get_db(database=None):

    if database is None:
        database = DATABASE

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row

    return conn


def create_table(database=None):

    conn = get_db(database)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TEXT,
            expires_at TEXT
        )
    """)

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