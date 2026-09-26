from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_shorten_url(client):

    response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "short_code" in data
    assert "short_url" in data
    assert "created_at" in data


def test_missing_url():
    client = app.test_client()

    response = client.post(
        "/shorten",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "JSON body is required"


def test_invalid_url():
    client = app.test_client()

    response = client.post(
        "/shorten",
        json={
            "url": "amazon.in"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid URL. Please provide a valid http:// or https:// URL"


def test_url_must_be_string():
    client = app.test_client()

    response = client.post(
        "/shorten",
        json={
            "url": 12345
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "URL must be a string"


def test_invalid_expiration():
    client = app.test_client()

    response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com",
            "expires_in": "abc"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "expires_in must be a number"


def test_negative_expiration():
    client = app.test_client()

    response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com",
            "expires_in": -60
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "expires_in must be greater than 0"
    
def test_get_all_urls():
    client = app.test_client()

    response = client.get("/urls")

    assert response.status_code == 200

    data = response.get_json()

    assert "count" in data
    assert "urls" in data

    assert isinstance(data["count"], int)
    assert isinstance(data["urls"], list)
    
def test_rate_limit(client):
    for _ in range(10):
        response = client.post(
            "/shorten",
            json={"url": "https://www.google.com"}
        )
        assert response.status_code == 201

    response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"}
    )

    assert response.status_code == 429