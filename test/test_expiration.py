from app import app
import time


def test_expired_url(client):

    # Create URL that expires in 1 second
    response = client.post(
        "/shorten",
        json={
            "url": "https://www.google.com",
            "expires_in": 1
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    short_code = data["short_code"]

    # Wait for URL to expire
    time.sleep(2)

    # Try to access expired URL
    response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert response.status_code == 410

    result = response.get_json()

    assert result["error"] == "Short URL has expired"