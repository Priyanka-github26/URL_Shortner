import pytest
import tempfile
import os

import database
import app


@pytest.fixture
def client(monkeypatch):

    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()

    # Create the temporary database tables
    original_database = database.DATABASE
    database.DATABASE = db_path

    database.create_table()

    # Make app.py use the temporary database
    def test_get_db():
        conn = database.sqlite3.connect(db_path)
        conn.row_factory = database.sqlite3.Row
        return conn

    monkeypatch.setattr(app, "get_db", test_get_db)

    # Also make database helper functions use temporary database
    monkeypatch.setattr(database, "get_db", test_get_db)

    with app.app.test_client() as client:
        yield client

    # Restore database
    database.DATABASE = original_database

    # Close and delete temporary database
    os.close(db_fd)
    os.unlink(db_path)