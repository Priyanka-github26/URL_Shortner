import pytest
import tempfile
import os

import database
from app import app


@pytest.fixture
def client():

    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()

    # Tell database.py to use temporary database
    database.DATABASE = db_path

    # Create tables in temporary database
    database.create_table()

    # Create Flask test client
    with app.test_client() as client:
        yield client

    # Close and delete temporary database
    os.close(db_fd)
    os.unlink(db_path)

    # Restore real database
    database.DATABASE = "urls.db"